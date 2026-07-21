// Подсказка
function hint()
{
  let answer = id("answer").value.toLowerCase().trim();
  if (answer == HINT)
  {
    document.getElementById("blockEnDET").style.display = "";
    document.getElementById("blockHint").style.display = "none";
  }
  else
  {
    id("err").style.display = "";
  }
}