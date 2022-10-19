
// Michael Bale and Rodrigo Bammann, Scientifica Ltd., UK adapted from https://forum.image.sc/t/using-a-macro-to-process-images-and-save-them-with-their-original-name/6643
// 01 March 2022
// Code to convert .raw

//Javid Added to convert to ome.tiff format for bigger files larger then 4 GB.


input = getDirectory("C:\YaksiData\ConversionFOolder");;
output = getDirectory("C:\YaksiData\ConversionFOolder");;

// function to scan folders/subfolders/files to find .raw files
function processFolder(input) {
list = getFileList(input);
for (i = 0; i < list.length; i++) {
if(File.isDirectory(input + File.separator + list[i]))
processFolder("" + input + File.separator + list[i]);
if(endsWith(list[i], "raw")) 
processFile(input, output, list[i]);
}
}

function processFile(input, output, file) {
name = input + File.getNameWithoutExtension(input + file) + '_IJmacro.txt';


runMacro(name);

run("OME-TIFF...","save=" +output + file +".ome.tiff" +" compression=Uncompressed");
close();
}

processFolder(input);
