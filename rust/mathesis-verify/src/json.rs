//! A minimal JSON parser, sufficient for `ledger.jsonl` rows.
//!
//! Written from scratch rather than pulled from crates.io on purpose. SPEC.md
//! §7.3 requires the Rust checker to share *no* dependency with the Python
//! reference — a differential gate whose two sides call the same JSON library
//! tests that library once and the ledger logic zero times.

use std::collections::BTreeMap;
use std::fmt;

#[derive(Debug, Clone, PartialEq)]
pub enum Value {
    Null,
    Bool(bool),
    Number(f64),
    String(String),
    Array(Vec<Value>),
    Object(BTreeMap<String, Value>),
}

impl Value {
    pub fn as_str(&self) -> Option<&str> {
        match self {
            Value::String(s) => Some(s),
            _ => None,
        }
    }

    pub fn as_array(&self) -> Option<&[Value]> {
        match self {
            Value::Array(v) => Some(v),
            _ => None,
        }
    }

    pub fn get(&self, key: &str) -> Option<&Value> {
        match self {
            Value::Object(map) => map.get(key),
            _ => None,
        }
    }

    pub fn is_object(&self) -> bool {
        matches!(self, Value::Object(_))
    }
}

#[derive(Debug)]
pub struct ParseError {
    pub message: String,
}

impl fmt::Display for ParseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.message)
    }
}

fn err<T>(message: impl Into<String>) -> Result<T, ParseError> {
    Err(ParseError { message: message.into() })
}

pub fn parse(input: &str) -> Result<Value, ParseError> {
    let bytes: Vec<char> = input.chars().collect();
    let mut pos = 0usize;
    skip_ws(&bytes, &mut pos);
    let value = parse_value(&bytes, &mut pos)?;
    skip_ws(&bytes, &mut pos);
    if pos != bytes.len() {
        return err(format!("trailing input at character {pos}"));
    }
    Ok(value)
}

fn skip_ws(input: &[char], pos: &mut usize) {
    while *pos < input.len() && matches!(input[*pos], ' ' | '\t' | '\n' | '\r') {
        *pos += 1;
    }
}

fn parse_value(input: &[char], pos: &mut usize) -> Result<Value, ParseError> {
    if *pos >= input.len() {
        return err("unexpected end of input");
    }
    match input[*pos] {
        '{' => parse_object(input, pos),
        '[' => parse_array(input, pos),
        '"' => Ok(Value::String(parse_string(input, pos)?)),
        't' => parse_literal(input, pos, "true", Value::Bool(true)),
        'f' => parse_literal(input, pos, "false", Value::Bool(false)),
        'n' => parse_literal(input, pos, "null", Value::Null),
        c if c == '-' || c.is_ascii_digit() => parse_number(input, pos),
        c => err(format!("unexpected character {c:?} at {pos}")),
    }
}

fn parse_literal(
    input: &[char],
    pos: &mut usize,
    word: &str,
    value: Value,
) -> Result<Value, ParseError> {
    for expected in word.chars() {
        if *pos >= input.len() || input[*pos] != expected {
            return err(format!("expected `{word}` at {pos}"));
        }
        *pos += 1;
    }
    Ok(value)
}

fn parse_number(input: &[char], pos: &mut usize) -> Result<Value, ParseError> {
    let start = *pos;
    if *pos < input.len() && input[*pos] == '-' {
        *pos += 1;
    }
    while *pos < input.len() && (input[*pos].is_ascii_digit() || matches!(input[*pos], '.' | 'e' | 'E' | '+' | '-')) {
        *pos += 1;
    }
    let text: String = input[start..*pos].iter().collect();
    text.parse::<f64>()
        .map(Value::Number)
        .map_err(|_| ParseError { message: format!("invalid number `{text}` at {start}") })
}

fn parse_string(input: &[char], pos: &mut usize) -> Result<String, ParseError> {
    if input[*pos] != '"' {
        return err(format!("expected string at {pos}"));
    }
    *pos += 1;
    let mut out = String::new();
    while *pos < input.len() {
        match input[*pos] {
            '"' => {
                *pos += 1;
                return Ok(out);
            }
            '\\' => {
                *pos += 1;
                if *pos >= input.len() {
                    return err("unterminated escape");
                }
                match input[*pos] {
                    '"' => out.push('"'),
                    '\\' => out.push('\\'),
                    '/' => out.push('/'),
                    'b' => out.push('\u{0008}'),
                    'f' => out.push('\u{000C}'),
                    'n' => out.push('\n'),
                    'r' => out.push('\r'),
                    't' => out.push('\t'),
                    'u' => {
                        let mut code = 0u32;
                        for _ in 0..4 {
                            *pos += 1;
                            if *pos >= input.len() {
                                return err("truncated \\u escape");
                            }
                            let digit = input[*pos]
                                .to_digit(16)
                                .ok_or_else(|| ParseError { message: "bad hex in \\u escape".into() })?;
                            code = code * 16 + digit;
                        }
                        out.push(char::from_u32(code).unwrap_or('\u{FFFD}'));
                    }
                    c => return err(format!("unknown escape \\{c}")),
                }
                *pos += 1;
            }
            c => {
                out.push(c);
                *pos += 1;
            }
        }
    }
    err("unterminated string")
}

fn parse_array(input: &[char], pos: &mut usize) -> Result<Value, ParseError> {
    *pos += 1; // consume '['
    let mut items = Vec::new();
    skip_ws(input, pos);
    if *pos < input.len() && input[*pos] == ']' {
        *pos += 1;
        return Ok(Value::Array(items));
    }
    loop {
        skip_ws(input, pos);
        items.push(parse_value(input, pos)?);
        skip_ws(input, pos);
        if *pos >= input.len() {
            return err("unterminated array");
        }
        match input[*pos] {
            ',' => *pos += 1,
            ']' => {
                *pos += 1;
                return Ok(Value::Array(items));
            }
            c => return err(format!("expected `,` or `]` in array, found {c:?}")),
        }
    }
}

fn parse_object(input: &[char], pos: &mut usize) -> Result<Value, ParseError> {
    *pos += 1; // consume '{'
    let mut map = BTreeMap::new();
    skip_ws(input, pos);
    if *pos < input.len() && input[*pos] == '}' {
        *pos += 1;
        return Ok(Value::Object(map));
    }
    loop {
        skip_ws(input, pos);
        if *pos >= input.len() || input[*pos] != '"' {
            return err(format!("expected object key at {pos}"));
        }
        let key = parse_string(input, pos)?;
        skip_ws(input, pos);
        if *pos >= input.len() || input[*pos] != ':' {
            return err(format!("expected `:` after key `{key}`"));
        }
        *pos += 1;
        skip_ws(input, pos);
        let value = parse_value(input, pos)?;
        map.insert(key, value);
        skip_ws(input, pos);
        if *pos >= input.len() {
            return err("unterminated object");
        }
        match input[*pos] {
            ',' => *pos += 1,
            '}' => {
                *pos += 1;
                return Ok(Value::Object(map));
            }
            c => return err(format!("expected `,` or `}}` in object, found {c:?}")),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_a_ledger_shaped_row() {
        let value = parse(r#"{"id":"MX-A-0001","tier":"A","supports":["MX-A-0002"]}"#).unwrap();
        assert_eq!(value.get("id").unwrap().as_str(), Some("MX-A-0001"));
        assert_eq!(value.get("supports").unwrap().as_array().unwrap().len(), 1);
    }

    #[test]
    fn rejects_trailing_garbage() {
        assert!(parse(r#"{"a":1} nope"#).is_err());
    }

    #[test]
    fn handles_escapes_and_unicode() {
        let value = parse(r#"{"s":"a\"b\né"}"#).unwrap();
        assert_eq!(value.get("s").unwrap().as_str(), Some("a\"b\né"));
    }

    #[test]
    fn rejects_unterminated_string() {
        assert!(parse(r#"{"s":"oops}"#).is_err());
    }
}
