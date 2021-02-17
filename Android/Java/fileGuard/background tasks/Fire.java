import java.io.*;
import java.util.*;
import org.apache.commons.io.FileUtils;//use ver. 2.6

public class Fire
{

	//public Fire(Boolean isEncrypt, String path, int option, String command, String key)
	public static void main(String[] argv)
	{
		//beware command escape symbols! replaceAll("'", "\\\\'") then surround variables with ''
		
		Boolean isEncrypt = Boolean.parseBoolean(argv[0]);
		String path = "'" + argv[1].replaceAll("'", "\\\\'") + "'";//target path
		int option = Integer.parseInt(argv[2]);
		String command = argv[3];
		String key = argv[4];
		
		/*Boolean isEncrypt = false;
		String path = "'" + "/sdcard/FLM User Files/My Songs/".replaceAll("'", "\\\\'") + "'"; //target path
		int option = 0;
		String command = "";
		String key = "241,206,74,165,213,242,105,31,88,235,123,117,226,36,209,39,201,254,131,103,50,133,224,95,83,59,146,17,49,184,135,208,144,28,239,212,60,140,32,54,215,94,166,65,173,178,247,107,20,102,7,76,108,124,246,202,238,248,97,136,193,12,161,27,91,120,217,89,10,111,100,8,46,142,237,194,30,177,159,180,231,52,26,98,211,220,169,34,116,1,141,23,112,170,5,93,251,236,197,75,15,73,80,232,143,234,57,6,229,99,41,58,154,181,55,163,79,147,243,148,191,38,150,137,44,82,216,85,188,33,19,92,128,47,158,227,167,81,138,21,132,183,204,122,125,113,134,198,130,118,156,214,104,25,11,63,245,205,77,115,18,225,66,101,189,195,68,176,210,48,228,253,71,96,172,240,168,151,69,219,90,64,2,61,84,45,56,78,4,230,233,162,24,255,62,70,196,139,244,207,67,192,106,186,203,22,199,175,249,9,252,3,53,109,187,157,126,149,182,174,29,190,40,121,145,13,35,114,160,185,152,51,87,43,218,164,86,129,16,221,119,37,0,153,155,110,72,179,171,127,250,222,200,14,42,223";
		*/
		
		
		String[] extentions = {};
		String[] names = {};
		String[] shCmd = {"sh", "-c", ""};
        int totalFiles = 0;		
		
		
		try
		{
			switch (option)
			{
				case 0:
					shCmd[2] = "find " + path + " -type f ";
					break;
				case 1:
				case 2:
					extentions = command.replace("/", "/.").split("/");
					extentions[0] = "." + extentions[0];
					shCmd[2] = "find " + path + " -type f ";
					break;
				case 3:
				case 4:
					names = command.split("/");
					if(option == 3 || option == 4)
					{
						for(int i = 0; i < names.length; i++)
						{
							names[i] = "'" + names[i].replaceAll("'", "\\\\'") + "'";
						}
					}
					shCmd[2] = "find " + path + " -type f ";
					break;
			}

			switch (option)
			{
				case 0://everything
					if (isEncrypt)
						shCmd[2] += "-not -name *.+enc";
					else
						shCmd[2] += "-name *.+enc";
					break;
				case 1://include ext
					for (int i = 0; i < extentions.length; i++)
					{
						if (isEncrypt)
							shCmd[2] += "-name *" + extentions[i];
						else
							shCmd[2] += "-name *" + extentions[i] + ".+enc";
						if (i < extentions.length - 1)
							shCmd[2] += " -o ";
					}

					break;
				case 2://exclude ext
					for (int i = 0; i < extentions.length; i++)
					{
						if (isEncrypt)
							shCmd[2] += "-not -name *" + extentions[i] + " ";
						else
							shCmd[2] += "-not -name *" + extentions[i] + ".+enc ";
					}
                    if (isEncrypt)
                        shCmd[2] += " -not -name *.+enc";
                    else 
                        shCmd[2] += " -name *.+enc";
					break;
				case 3://include name
					for (int i = 0; i < names.length; i++)
					{
						if (isEncrypt)
							shCmd[2] += "-name " + names[i];
						else
							shCmd[2] += "-name " + names[i] + ".+enc";
						if (i < names.length - 1)
							shCmd[2] += " -o ";
					}
					break;
				case 4://exclude name
					for (int i = 0; i < names.length; i++)
					{
						if (isEncrypt)
							shCmd[2] += "-not -name " + names[i] + " ";
						else
							shCmd[2] += "-not -name " + names[i] + ".+enc ";
					}
                    if (isEncrypt)
                        shCmd[2] += "-not -name *.+enc";
                    else 
                        shCmd[2] += "-name *.+enc";
					break;
			}
			shCmd[2] += " >/sdcard/file_result.txt";
			Runtime.getRuntime().exec(shCmd).waitFor();

			//Do the main jobs

			String[] keyStr = key.split(",");
			int[] intKeyStr = new int[256];
			for (int i = 0; i < 256; i++)intKeyStr[i] = Integer.parseInt(keyStr[i]);//generate key array

			File f = new File("/sdcard/file_result.txt");
			Scanner sc = new Scanner(f);


            int fileCount = 1;
            while (sc.hasNextLine())
            {
                sc.nextLine();
                totalFiles++;
            }

            sc = new Scanner(f);
            //clear file list txt
			f.delete();

			if (isEncrypt)
			{
				while (sc.hasNextLine())
				{
					fileMod(new File(sc.nextLine()), intKeyStr, isEncrypt, fileCount, totalFiles);
                    fileCount++;
				}
			}
			else
			{
				int[] revIntKeyStr = new int[256];
				for (int i = 0; i < 256; i++)revIntKeyStr[intKeyStr[i]] = i;//swapping indices

				while (sc.hasNextLine())
				{
					fileMod(new File(sc.nextLine()), revIntKeyStr, isEncrypt, fileCount, totalFiles);
                    fileCount++;
				}
			}
            
		}
		catch (Exception e)
		{
			System.out.println(e.toString());
		}
        if(isEncrypt)
            System.out.println(String.format("Finished encrypting %d files (If no errors). Command FYR: %s", totalFiles, shCmd[2]));
        else
            System.out.println(String.format("Finished decrypting %d files (If no errors). Command FYR: %s", totalFiles, shCmd[2]));

	}

	private static void fileMod(File f, int[] intKeyStr, Boolean isEncrypt, int fileCount, int totalFiles)
    {
        try
		{
            //read
            byte[] content = FileUtils.readFileToByteArray(f);
            int[] modByte = new int[content.length];

            //modify in memory
            int cumulatePt = (int)Math.floor(content.length * 0.1);
            int startPt = 0;
            for (int i = 0; i < 10; i++)
            {
                try
				{
                    for (int j = startPt; j < startPt + 100000; j++)
                    {
                        modByte[j] = content[j] & 0xff;
                        modByte[j] = intKeyStr[modByte[j]];//original bytes -> modded bytes
                        content[j] = (byte)modByte[j];
                    }
                    startPt += cumulatePt;
                }
				catch (Exception e)
				{}

            }
            
            //backup original file
			String source = "'" + f.getPath().replaceAll("'", "\\\\'") + "'";
			String destName = f.getName().replaceAll("'", "\\\\'");
            String[] mvCmd = {"sh", "-c", String.format("mkdir /sdcard/fileGuard & mv -f %s '/sdcard/fileGuard/%s'", source, destName)};
            Runtime.getRuntime().exec(mvCmd).waitFor();
			FileWriter origCPRef = new FileWriter(new File("/sdcard/fileGuard/path_of_" + f.getName() + ".txt"));
            origCPRef.write(f.getParent());
            origCPRef.close();

            //output bytes to file
            FileOutputStream fos; 

			if (isEncrypt)
			{
				File outFile = new File(f.getPath() + ".+enc");
				outFile.createNewFile();
                fos = new FileOutputStream(outFile.getPath());
				System.out.println(String.format("[%d/%d] Encrypted: %s...",fileCount, totalFiles, f.getPath()));
			}
			else
			{
				File outFile = new File(f.getPath().substring(0, f.getPath().length() - 5));
				outFile.createNewFile();
                fos = new FileOutputStream(outFile.getPath());
				System.out.println(String.format("[%d/%d] Decrypted: %s...",fileCount, totalFiles, f.getPath()));
			}
            fos.write(content);
            fos.close();

            //erase backup
            File backupCP = new File("/sdcard/fileGuard/" + f.getName());
            File backupDel = new File(backupCP.getPath() + ".deletable");
			backupCP.renameTo(backupDel);
			backupDel.delete();
            new File("/sdcard/fileGuard/path_of_" + f.getName() + ".txt").delete();
            
        }
		catch (Exception e)
		{System.out.println(e.toString());}
    }

}
