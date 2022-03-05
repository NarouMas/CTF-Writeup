from Wappalyzer import Wappalyzer, WebPage

wapplyzer = Wappalyzer.latest()
webpage = WebPage.new_from_url("https://www.nchu.edu.tw/index1.php")
result = wapplyzer.analyze(webpage)
print(result)