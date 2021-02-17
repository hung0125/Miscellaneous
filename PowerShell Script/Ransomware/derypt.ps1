#Functions

Function genRevKey($keyNums)
{
    $revKeyNums = 0..255
    for($i = 0; $i -lt 256; $i++)
    {
        $revKeyNums[$keyNums[$i]] = $i    
    }
    $revKeyNums
}


Function decrypt($keyNums)
{

    $file = "test/encrypted.png"
    [byte[]]$fileBytes = Get-Content $file -Encoding Byte

    for($i = 0; $i -lt $fileBytes.Length; $i++)
    {
        $fileBytes[$i] = $revkeyNums[$fileBytes[$i]] #shift bytes
    }

    set-content "test/decrypted.png" -value $fileBytes -Encoding Byte
}

#Main Program

$keyNums = "".split(",")
$revKeyNums = genRevKey $keyNums

decrypt $revKeyNums
#Main Program


