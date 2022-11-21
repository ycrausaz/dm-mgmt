Attribute VB_Name = "Module1"
Option Explicit

Function RandomString(Length As Integer) As String
'PURPOSE: Create a Randomized String of Characters
'SOURCE: www.TheSpreadsheetGuru.com/the-code-vault

Dim CharacterBank As Variant
Dim x As Long
Dim str As String

'Test Length Input
  If Length < 1 Then
    MsgBox "Length variable must be greater than 0"
    Exit Function
  End If

CharacterBank = Array("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", _
  "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", _
  "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "@", _
  "#", "$", "%", "^", "&", "*", "A", "B", "C", "D", "E", "F", "G", "H", _
  "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", _
  "W", "X", "Y", "Z", _
  "‰", "", "”", "™", "ž", _
  "‡", "Ž", "’", "—", "œ", _
  "ˆ", "", "“", "˜", "ž", _
  "Š", "‘", "•", "š", "Ÿ")
  

'Randomly Select Characters One-by-One
  For x = 1 To Length
    Randomize
    str = str & CharacterBank(Int((UBound(CharacterBank) - LBound(CharacterBank) + 1) * Rnd + LBound(CharacterBank)))
  Next x

'Output Randomly Generated String
  RandomString = str

End Function

Function RandomInt(min As Integer, max As Integer) As Integer
Dim ret As Integer

ret = Int((max - min + 1) * Rnd() + min)

RandomInt = ret
End Function

Function RandomDate(minDate As Date, maxDate As Date)
    RandomDate = WorksheetFunction.RandBetween(minDate, maxDate)
End Function

Function randomBool() As String
    If Rnd() > 0.5 Then
        randomBool = "t"
    Else
        randomBool = "f"
    End If
End Function



