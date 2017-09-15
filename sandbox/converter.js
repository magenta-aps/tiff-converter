var fso = new ActiveXObject("Scripting.FileSystemObject");
var objWord = null;
var wdFormatPdf = 17;

try
{
//	WScript.Echo("Saving '" + docPath + "' as '" + pdfPath + "'...");

	objWord = new ActiveXObject("Word.Application");
	objWord.Visible = false;

	for (var i = 0; i < 10; i++) {
		docPath = fso.GetAbsolutePathName("docs") + "\\demo" + i + ".docx";
//		WScript.echo(docPath);
		var objDoc = objWord.Documents.Open(docPath);
		var pdfPath = docPath.replace(/\.doc[^.]*$/, ".pdf");
		pdfPath = pdfPath.replace("docs", "pdfs");

//		WScript.echo(pdfPath);

		objDoc.SaveAs(pdfPath, wdFormatPdf);
		objDoc.Close();
	}

	WScript.Echo("Done.");
}
finally
{
	if (objWord != null)
	{
		objWord.Quit();
	}
}
