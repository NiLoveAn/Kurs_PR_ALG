; ModuleID = "/home/andrey/PycharmProjects/Compiler/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"()
{
entry:
  %"a" = alloca i32
  store i32 10, i32* %"a"
  %"b" = alloca i32
  store i32 2, i32* %"b"
  %"s" = alloca i32
  store i32 1, i32* %"s"
  br label %"condit_block"
condit_block:
  %".6" = load i32, i32* %"b"
  %".7" = icmp sgt i32 %".6", 0
  br i1 %".7", label %"body_block", label %"after_block"
body_block:
  %".9" = load i32, i32* %"b"
  %".10" = srem i32 %".9", 2
  %".11" = icmp ne i32 %".10", 0
  br i1 %".11", label %"if_block", label %"after_block.1"
after_block:
  %".31" = load i32, i32* %"s"
  %".32" = bitcast [5 x i8]* @"fstr1" to i8*
  %".33" = call i32 (i8*, ...) @"printf"(i8* %".32", i32 %".31")
  ret void
if_block:
  %".13" = load i32, i32* %"s"
  %".14" = load i32, i32* %"a"
  %".15" = mul i32 %".13", %".14"
  store i32 %".15", i32* %"s"
  br label %"after_block.1"
after_block.1:
  %".18" = load i32, i32* %"b"
  %".19" = load i32, i32* %"b"
  %".20" = srem i32 %".19", 2
  %".21" = sub i32 %".18", %".20"
  %".22" = sdiv i32 %".21", 2
  store i32 %".22", i32* %"b"
  %".24" = load i32, i32* %"a"
  %".25" = load i32, i32* %"a"
  %".26" = mul i32 %".24", %".25"
  store i32 %".26", i32* %"a"
  %".28" = load i32, i32* %"b"
  %".29" = icmp sgt i32 %".28", 0
  br i1 %".29", label %"body_block", label %"after_block"
}

declare i32 @"printf"(i8* %".1", ...)

@"fstr1" = internal constant [5 x i8] c"%i \0a\00"