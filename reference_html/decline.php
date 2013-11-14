<HTML>
<title>CCPP Astrocoffee</title>
  <HEAD>
    <LINK href="style.css" rel="stylesheet" type="text/css">
  </HEAD>
<div class=page>
  <h1>CCPP Astrocoffee</h1>
     <br><p>
        <h3> Shucks! </h3><br>
        <?php
   
function check_date($date) 
{
  $ok = TRUE;
  if ((strlen($date) != 6) or ((int) substr($date, 0, 2) > 31) 
      or ((int) substr($date, 0, 2) < 1) or ((int) substr($date, 2, 2) < 1)
      or ((int) substr($date, 2, 2) > 12) or ((int) substr($date, 4, 2) < 13))
    {
      $ok = FALSE;
    }
  
  return $ok;
}

function message($ok, $phrase, $kind, $date, $today)
{
  if ($ok) {
       echo "<div class=flash>We got ya, $phrase</div>";
       record($kind, $date, $today);
     }
  else
    {
      echo "<div class=error>Whoops, wrong format (DDMMYY).  Please go back and re-submit!</div.";
    }
}

function record($kind, $date, $today)
{
  $f = fopen("answer_%s.txt", "w");
  fwrite($f, "$kind $date $today");
  fclose($f);
}

   $gone = $_POST["gone"];
   $willgo = $_POST["willgo"];

   if (gettype($gone) != "NULL") 
   { 
     $date = $gone;
     $dd = substr($date, 0, 2);
     $mm = substr($date, 2, 2);
     $yy = substr($date, 4, 2);
     $phrase = "you are gone until $dd-$mm-20$yy (DD-MM-YYYY)";
     $kind = 'gone';
   }
   if (gettype($willgo) != "NULL")
   {
     $date = $willgo;
     $dd = substr($date, 0, 2);
     $mm = substr($date, 2, 2);
     $yy = substr($date, 4, 2);
     $phrase = "you will next present on $dd-$mm-20$yy (DD-MM-YYYY).";
     $kind = 'willgo';
   }

$today = date(DATE_ATOM);
$ok = check_date($date);
message($ok, $phrase, $kind, $date, $today);

?>

  </div>
</HTML>
