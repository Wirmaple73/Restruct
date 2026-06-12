from sys import stderr, argv
from re import split

def remove_empty_entries(strList, trimEntries: bool = True):
	return [s.strip() for s in strList if len(s) > 0] if trimEntries else [s for s in strList if len(s) > 0]

def parse_properties(target: str):
	# For example, 'target' can be "size: 4, offset: 0xC2, comment: Figure out what it does"

	parts = remove_empty_entries(target.split(","))
	propDict = {}

	for part in parts:
		prop = remove_empty_entries(split(r"[:=]", part))

		if len(prop) == 2:
			propDict[prop[0].lower()] = prop[1]

	return propDict

def parse_int(target: str) -> int:
	return int(target, 16 if "0x" in target.lower() else 10)

class StructField:
	_declaration: str

	_size: int
	_offset: int

	def __init__(self, declaration: str):
		parts = remove_empty_entries(declaration.split("//"))

		if len(parts) < 2:
			raise SyntaxError("Could not find a valid field declaration.")

		self._declaration = parts[0]
		props = parse_properties(parts[1].lower())

		if "size" not in props or "offset" not in props:
			raise SyntaxError("Could not find the explicit size and offset of this field.")

		self._size = parse_int(props["size"])
		self._offset = parse_int(props["offset"])

	def get_declaration(self) -> str:
		return self._declaration

	def get_offset(self) -> int:
		return self._offset

	def get_size(self) -> int:
		return self._size

def abort(message: str, code: int = 1) -> None:
	stderr.write(message + "\n")
	exit(code)


if len(argv) < 3:
	abort(f"USAGE: {argv[0]} <input file> <output file>")

inputFile = argv[1]

with open(inputFile) as file:
	content = file.read().strip()

tokens = content.split()

if len(tokens) < 2 or tokens[0].lower() not in ["class", "struct"]:
	abort("The name of the class or struct could not be detected.")

startBraceIndex = content.find("{")
endBraceIndex = content.find("}")

if startBraceIndex == -1 or endBraceIndex == -1 or startBraceIndex > endBraceIndex:
	abort("No matching '{' and '}' could be found.")

objectType = tokens[0]  # e.g. "struct"
objectName = tokens[1]  # e.g. "Vehicle"
outputFile = argv[2]

fields = [line.strip() for line in content[startBraceIndex + 1:endBraceIndex].splitlines() if line != ""]  # Now each element contains a struct field

paddingIndex = 1
previousOffset = previousSize = 0x0

with open(outputFile, "w") as file:
	file.write(f"{objectType} {objectName}\n")
	file.write("{\n")

	for field in fields:
		sf = StructField(field)
		offset = sf.get_offset() - previousOffset - previousSize

		file.write(f"\tchar Padding{paddingIndex}[0x{offset:X}];\n")
		file.write("\t" + sf.get_declaration() + "\n")

		paddingIndex += 1

		previousOffset = sf.get_offset()
		previousSize = sf.get_size()

	file.write("};")

print("The input file has been successfully converted.")
