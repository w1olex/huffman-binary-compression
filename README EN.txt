(translated via ChatGPT cuz im lazy lmao):



FILE COMPRESSION


Example usage:

For naming files and folders, you can only use basic characters - that is, small and capital letters of the English alphabet and numbers 0-9.

COMPRESSION

First, ensure that you have your file.txt that you want to compress in the /txt/ folder.

Run the program and choose the compression option (type 'k' in the console line).

Enter the name of your file without the .txt extension.

Enter how you want to name the output file.

After successful compression, this output binary file will be saved in the /outputs/ folder.

At the same time, a Codeword Table and a Frequency Table will be saved in the /data/ folder, these are only for interest, when compressing another file.txt it will be overwritten.



DECOMPRESSION

If you have your compressed binary file saved in the /outputs/ folder, you are ready for decompression.

Enter the name of this binary file without the .bin extension.

Enter how you want to name your output file (without the .txt extension).

Enter the name of the folder where you want to save this file.

If decompression was successful, you should have a file.txt in the folder you selected that contains the text of the originally compressed file.



My test:

The file I tested, 'test.txt' located in the /txt/ folder, had a size of 175 kB before compression. I named the compressed file 'testCompression.bin' (saved in the /outputs/ folder) and it has a size of 96 kB.

Then I decompressed the file 'testCompression.bin', I named the output file 'testDecompression.txt' and saved it in the 'testDecompression' folder.

As you can see, the file has the same size of 175 kB, contains the same text as the 'test.txt' file, so my program works perfectly.