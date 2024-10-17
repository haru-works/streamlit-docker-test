function downloadFile(file, fileName) {
    // ファイルをBlobに変換
    const blob = new Blob([file], { type: getMimeType(fileName) });
  
    // Python側の関数を呼び出す
    streamlit.components.v1.html("pythonFunctionName", { fileData: blob }); 
  }
  
  function getMimeType(fileName) {
    const extension = fileName.split('.').pop().toLowerCase(); // 拡張子を小文字に変換
    const mimeTypes = {
      'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'txt': 'text/plain',
      'pdf': 'application/pdf',
      'csv': 'text/csv',
      'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    };
    return mimeTypes[extension] || 'application/octet-stream'; // 拡張子が不明な場合は汎用的なMIMEタイプ
  }
  
  async function fetchData(url, fileName) { // 引数でURLとファイル名を受け取る
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }
      const fileBlob = await response.blob();
      downloadFile(fileBlob, fileName); // ファイル名をダウンロード関数に渡す
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }
  
  // Python側から渡された引数を受け取る
  const url = streamlit.components.v1.getArgs().url; // API URL
  const fileName = streamlit.components.v1.getArgs().fileName; // ファイル名
  fetchData(url, fileName); // 引数を渡して fetchData を呼び出す