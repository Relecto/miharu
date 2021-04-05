
CHARS =  { '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!' }


def escape(string):
  i = 0
  while i < len(string):
    if string[i] in CHARS:
      string = string[:i] + '\\' + string[i:]
      i += 1
    i += 1

  return string
