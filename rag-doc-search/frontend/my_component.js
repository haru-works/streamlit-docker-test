function downloadFile(file) {
    // ファイルをBlobに変換
    const blob = new Blob([file], { type: file.type });
  
    // Python側の関数を呼び出す
    // 'pythonFunctionName' はPython側の関数の名前です。
    // 'fileData' はPython側に渡すファイルデータです。
    streamlit.components.v1.html("pythonFunctionName", { fileData: blob }); 
  }
  
  async function fetchData() {
    try {
      const response = await fetch("https://example.com/api/file"); // APIエンドポイントを指定
      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }
      const fileBlob = await response.blob();
      downloadFile(fileBlob);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }
  
  fetchData();