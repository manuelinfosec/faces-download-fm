# Football Manager Face Downloader

The **Football Manager Face Downloader** script automates the download of player face images for a specified division from SortitoutSI or by extracting "Unique IDs" from a CSV file. It is designed for Football Manager enthusiasts who want to quickly fetch and organize player images without having to download the entire facepack.

---

## **Features**

- Download player face images for an entire division by providing a SortitoutSI division link.
- Parse a CSV file containing player "Unique IDs" to download specific player images.
- Asynchronous downloads for maximum efficiency.
- Automatic skip for already downloaded images.
- Logs progress and summarizes the total downloads and time taken.

---

## **Usage**

### **1. Download Images for a Division**

Use the script to download images for a specific division by providing a SortitoutSI division link:

```bash
python faces.py <sortitoutsi_division_link>
```

#### Example:

```bash
python faces.py https://sortitoutsi.net/football-manager-2024/competition/102421/argentine-premier-division
```

### **2. Download Images Using a CSV File**

If you have a CSV file containing player information with "Unique IDs," use this command:

```bash
python faces.py <CSV file path>
```

#### Example:

```bash
python faces.py players.csv
```

---

## **CSV Requirements**

- The CSV file must contain a column named `Unique ID`.
- Ensure the file is correctly formatted for the script to process it successfully.
- For larger datasets, improve efficiency by retaining only the `Unique ID` column and removing all other columns from the CSV file.

#### Example CSV Structure:

```csv
"Name","Nation","Position","Club","Jdns","Con","Happiness Level","Age","Int Caps","Int Goals","Wage","Value","Sale Value","Best Rating","Best Pot Rating","Unique ID"
"John Doe","England","Midfielder","Club A","123","90","Happy","25","5","2","50k","10M","12M","8","9","1234567"
"Jane Doe","Brazil","Forward","Club B","456","85","Very Happy","23","10","8","60k","15M","20M","9","10","7654321"
```

---

## **Setup**

1. **Install Dependencies**
   The script requires Python 3.8+ and the following libraries:

   - `aiohttp`
   - `beautifulsoup4`

   Install them using pip:

   ```bash
   pip install aiohttp beautifulsoup4
   ```

2. **Prepare a Destination Directory**
   The script automatically should be executed in the Football Manager `graphics` directory to store the downloaded images. Alternatively, you can run in any other directory and manually move the images to the `graphics` directory.

---

## **Output**

1. **Logs Progress**  
   The script logs messages for each download attempt:

   ```
   2024-11-22 15:00:00 - INFO - Downloaded: 12345.png
   2024-11-22 15:00:01 - INFO - Already exists: 67890.png
   ```

2. **Summary of Resources**  
   At the end of execution, a summary is displayed:
   ```
   Downloaded 217830 new images in 45.23 seconds.
   ```

---

---

## **Examples**

### Example 1: Division Download

```bash
python faces.py https://sortitoutsi.net/football-manager-2024/competition/102421/argentine-premier-division
```

### Example 2: CSV-Based Download

```bash
python faces.py players.csv
```
