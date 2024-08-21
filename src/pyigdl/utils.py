import re
from urllib.parse import unquote

def extractEncodedComponent(s):
  x = re.search("decodeURIComponent\(.*\)}\(\"([a-zA-Z0-9]+)\",[a-zA-Z0-9]+,\"([a-zA-Z0-9]+)\",", s)
  if x:
    return [x.group(1), x.group(2)]
  return None
  
def convertExtractedComponentToParseableOutput(s):
  a, b = extractEncodedComponent(s)
  components = a.split(b[2])
  for c in range(len(components)):
    components[c] = components[c].replace(b[0], '0')
    components[c] = components[c].replace(b[1], '1')
  binary_variations = []
  for c in components:
    if c != "":
      binary_variations.append(int(c, 2) - 1)
  return unquote(''.join(map(chr, binary_variations)))

def extractHtmlContentFromJsResponse(s):
  js = convertExtractedComponentToParseableOutput(s)
  interim = js.split(".innerHTML")[1].strip().split(";")[0].strip()
  start = interim.find("<ul")
  interim = interim[start:-1]
  interim = interim.replace("\\\"", "\"")
  return interim
