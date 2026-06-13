<p align="center">
	<h3 align="center">In the Name of God</h3>
</p>

## 🔢🔧 Restruct
A little script designed for folks (mostly reverse engineers) who need to use custom offsets in their structs. Instead of writing padding bytes by hand, which is cumbersome and prone to errors, let Restruct automate it!

[![MIT License](https://img.shields.io/badge/license-MIT-forestgreen)](LICENSE)

## ⬇ Installation
Ensure Python `3.8` or greater is installed. Now, either download this repo or run the following commands in the terminal:
```cmd
git clone https://github.com/Wirmaple73/Restruct.git
cd Restruct
```

## ▶ Usage
The following steps assume you have completed the installation guide above.

1. Declare your class or struct of choice in `input.txt`:
```cpp
struct Character
{
	int Handle;				  // size: 4, offset: 0x0
	char* Name;				  // size: 4, offset: 0x4
	float Health;  			  // size: 4, offset: 0x64
	bool IsInvulnerable;	  // size: 1, offset: 0xEA
	double Coords[3];		  // size: 24, offset: 0xF2
	Vehicle* CurrentVehicle;  // size: 4, offset: 0x11A
};
```

**Notes:**
* Mixing decimal and hexadecimal numbers is fine. All numbers are interpreted as decimal, except those beginning with `0x`.
* You may also use `=` instead of `:` when specifying field properties.
* After each field declaration, you **always** have to explicitly specify its `size` and `offset` properties as shown above. You can write the properties in any order.
* Whitespace and indentation don't matter.
* Less common declarations like `typedef struct { ... }` or `struct __declspec(...)` are not supported. The only supported declarations are `struct Name` and `class Name`.

2. Now just run `run.bat`. A new file called `Output.txt` will be generated in the same directory like so:
```cpp
struct Character
{
	int Handle;
	char* Name;
	char Padding1[0x5C];
	float Health;
	char Padding2[0x84];
	bool IsInvulnerable;
	char Padding3[0x5];
	double Coords[3];
	char Padding4[0x10];
	Vehicle* CurrentVehicle;
};
```
3. ???
4. PROFIT!!1

**Note:** You can configure the input and output files as needed by running `python main.py path/to/input.txt path/to/output.txt` instead.

## 💬 Feedback & Contributions
Feel free to [report bugs and request new features](https://github.com/Wirmaple73/Restruct/issues). Contributions are very welcome, too. If you think this script is cool, please feel free to spare a star!
