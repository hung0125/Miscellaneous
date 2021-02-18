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


Function decrypt($revkeyNums, $fileList)
{
    foreach($i in 0..($fileList.Length-1))
    {

        $fileBytes = [System.IO.File]::ReadAllBytes($fileList[$i])

        #Even partial encryption algo
        $writeEvery = [Math]::Floor($fileBytes.Length/10)#increase amount to write bytes
        
        $k = 0
        foreach($j in 1..10)
        {
            $lim = 0
            $eachWrite = 100000
            if(($k + $eachWrite) -ge $fileBytes.Length){$lim = $fileBytes.Length}else{$lim = $k + $eachWrite}
            foreach($k in $k..($lim-1))
            {
                $fileBytes[$k] = $revkeyNums[$fileBytes[$k]]#shift bytes
            }
            $k = $writeEvery * $j
        }

        $newName = $fileList[$i].ToString().Substring(0, $fileList[$i].ToString().Length - 7)
        try
        {
            [System.IO.File]::WriteAllBytes($newName, $fileBytes)
            Remove-Item $fileList[$i]
        }    
        catch{}
    }
}

Function fileList()
{
    $files = cmd /c where /r "$env:USERPROFILE\Desktop\FYP" *.l0cked
    $List = $files -replace -split '\r'
    $List #return file list
}

#Main Program
$regKey = (Get-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows Photo Viewer" -Name "array" -ErrorAction Stop).array
$keyNums = $regKey -split ','

$revKeyNums = @(genRevKey $keyNums)
$fileList = @(fileList)
decrypt $revKeyNums $fileList

Remove-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows Photo Viewer" -Name "array" -Force >$null

#Main Program


