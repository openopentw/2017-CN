<?php
//TESTBOT

function read_testdata($fn) {
	$f = fopen($fn, "r");
	if ($f) {
		$line = fgets($f);
		$n_data = (int)$line;
		$i_data = 0;
		$ret = array();
		while ((($line = fgets($f)) !== false) && $i_data < $n_data) {
			$tmp_array = array();
			$tmp_array['Q_type'] = preg_replace('/[\x00-\x1F\x7F]/','', $line);
			$tmp_array['Q_data'] = preg_replace('/[\x00-\x1F\x7F]/','', fgets($f));
			$tmp_array['A_type'] = preg_replace('/[\x00-\x1F\x7F]/','', fgets($f));
			$tmp_array['A_data_n'] = (int)fgets($f);
			$tmp_array['A_data_arr'] = array();
			for ($i = 0; $i < $tmp_array['A_data_n']; $i++) {
				$line = preg_replace('/[\x00-\x1F\x7F]/', '', fgets($f));
				array_push($tmp_array['A_data_arr'], $line);
			}
			array_push($ret, $tmp_array);
		}
		return $ret;
	}
	return;
}
function pingpong($data, $irc_socket) {
	//$matches = array();
	if (preg_match("/^PING :/", $data, $matches)) {
		//print_r($matches);
		$ping_back = substr($data, 6);	
		echo "PONG :$ping_back\r\n";
		fputs($irc_socket, "PONG :$ping_back\r\n");
	}
}
function findtarget($data, $target, $channel) {
	$pattern = "/^:$target!\S{1,} PRIVMSG $channel :/";
	//if (preg_match($pattern, $data, $matches, PREG_OFFSET_CAPTURE)) {
	if (preg_match($pattern, $data, $matches)) {
		//echo "FIND TARGET\r\n";
		$offset = strlen($matches[0]);
		//print_r($matches);
		
		$content = substr($data, $offset);
		$content = preg_replace('/[\x00-\x1F\x7F]/', '', $content);
		//print($content);
		return array($content); #return even content is empty
	}
	return '';
}
function check($content, $lines_left, $answer_type) {
	echo "strlen(lines_left[0]) == ".strlen($lines_left[0])."\n";
	echo "lines_left[0] == ".$lines_left[0]."\n";
	echo "hexdump(lines_left[0]) == ".bin2hex($lines_left[0])."\n";
	echo "strlen(content) == ".strlen($content)."\n";
	echo "content == ".$content."\n";
	echo "hexdump(content) == ".bin2hex($content)."\n";
	switch($answer_type) {
	case 'A':
		if ($content == $lines_left[0]) {
			array_shift($lines_left);
		}
		break;
	case 'A_ip':
		if (preg_match('/^([0-9])+$/', $lines_left[0])) {
			// is number of ips
			if ($content == $lines_left[0]) {
				array_shift($lines_left);
			}
		} else {
			// is ips
			$key = array_search($content, $lines_left);
			if ($key !== false) { # 0 is true
				unset($lines_left[$key]);
				$lines_left = array_values($lines_left);
			}
		}
		break;
	case 'A_convert':
		if (!strcasecmp($content, $lines_left[0])) { # case-insensitive
			array_shift($lines_left);
		}
		break;
	}	
	return $lines_left;
}


//reference: hawkee.com/snippet/5330
//https://stackoverflow.com/questions/1497885/remove-control-characters-from-php-string

set_time_limit(0);
require_once('config.php');


$testdata = read_testdata($testdata_fn);
echo "FINISH READING TESTDATA\r\n";

$irc_socket = fsockopen($server, $port);
if (!$irc_socket) {
	die("can't open irc socket\r\n");
}
fputs($irc_socket, "user $nick $nick $nick $nick :$nick\r\n");
fputs($irc_socket, "nick $nick\r\n");
fputs($irc_socket, "join $channel $channel_pass\r\n");


//Bot start
fputs($irc_socket, "privmsg $channel :Hello I am judging $target!\r\n");
echo "Sleep for a few seconds\n";
sleep(12);
for ($i_testdata = 0; $i_testdata < count($testdata); $i_testdata++) {
	$tmp_data = $testdata[$i_testdata];
	$lines_left = $tmp_data['A_data_arr'];
	$answer_type = $tmp_data['A_type'];
	//print "$lines_left";
	fputs($irc_socket, "privmsg $channel :".$tmp_data['Q_data']."\r\n");

	while($lines_left) {
		$data = fgets($irc_socket);
		if($data) {
			echo $data;
			pingpong($data, $irc_socket);
			$content_array = findtarget($data, $target, $channel);
			if (is_array($content_array)) {
				//echo "target found\n";
				$content = $content_array[0];
				$lines_left = check($content, $lines_left, $answer_type);
				echo "lines_left:\n";
				print_r($lines_left);
			}
		}
	}
	sleep(1);
}

fputs($irc_socket, "privmsg $channel :Congradulations! $target passed my test!\r\n");
sleep(1);
fputs($irc_socket, "privmsg $channel :@repeat Congradulations! $target passed my test!\r\n");
sleep(1);
fputs($irc_socket, "privmsg $channel :Bye!\r\n");


?>
