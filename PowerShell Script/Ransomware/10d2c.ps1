function encrypt()
{

}

$getUUID = (Get-WmiObject -Class Win32_ComputerSystemProduct).UUID;
$UUID = $getUUID.split("-")[4];
