// ----------------------------------------------------
  // Use these functions as is to perform required Streamlit
  // component lifecycle actions:
  //
  // 1. Signal Streamlit client that component is ready
  // 2. Signal Streamlit client to set visible height of the component
  //    (this is optional, in case Streamlit doesn't correctly auto-set it)
  // 3. Pass values from component to Streamlit client
  //

  // Helper function to send type and data messages to Streamlit client
  const SET_COMPONENT_VALUE = "streamlit:setComponentValue";
  const RENDER = "streamlit:render";
  const COMPONENT_READY = "streamlit:componentReady";
  const SET_FRAME_HEIGHT = "streamlit:setFrameHeight";

  function _sendMessage(type, data) {

    var outboundData = Object.assign({
        isStreamlitMessage: true,
        type: type,
      }, data);

    if (type == SET_COMPONENT_VALUE) {
        //console.log("_sendMessage data: " + JSON.stringify(data))
        //console.log("_sendMessage outboundData: " + JSON.stringify(outboundData))
    };
    window.parent.postMessage(outboundData, "*");
  };

  function initialize(pipeline) {

    // Hook Streamlit's message events into a simple dispatcher of pipeline handlers
    window.addEventListener("message", (event) => {
      if (event.data.type == RENDER) {
        // The event.data.args dict holds any JSON-serializable value
        // sent from the Streamlit client. It is already deserialized.
        pipeline.forEach(handler => {
          handler(event.data.args)
        })
      }
    });

    _sendMessage(COMPONENT_READY, { apiVersion: 1 });

    setFrameHeight(400);
  };

  function setFrameHeight(height) {
    _sendMessage(SET_FRAME_HEIGHT, { height: height })
  };

  // The `data` argument can be any JSON-serializable value.
  function notifyHost(data) {
    _sendMessage(SET_COMPONENT_VALUE, data)
  };

////////////////////////////////////////////////////////////////
    const ddZone = document.getElementById('dropArea');
    const uploadFile = document.getElementById('uploadFile');
    const uploadDirectory = document.getElementById('uploadDirectory');
    const msgLabel = document.getElementById("message_label")
    const username_label = document.getElementById("username_label")
    const collectionname_label = document.getElementById("collectionname_label")

    var ACCESS_TOKEN =null;
    
    const toBase64DataUri = file => new Promise(resolve => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.readAsDataURL(file);
      });

    const handleFiles = (files) => {
        dataFiles = []
        for  (let i = 0; i < files.length; i++) {

            username = username_label.innerHTML
            collectionname = collectionname_label.innerHTML

            const formData = new FormData();
            formData.append("username", username);
            formData.append("collectionname", collectionname);
            formData.append('upload_file', files[i]);
            const URL = "http://localhost:8000/api/v1/files/uploadfile/"
            const requestOptions={
                method:"POST",
                mode:"cors",
                headers: {
                    'Access-Control-Allow-Origin':'*',
                    'Authorization': 'Bearer '+ ACCESS_TOKEN,
                    'Accept': 'application/json',
                    
                },
                body:formData
            }
            fetch(URL, requestOptions)
                .then(response => {console.log(response)})


            dataFiles.push({"filename":files[i].name})
        }
        notifyHost({
            value: dataFiles,
            dataType: "json",
          });
    };


    uploadFile.addEventListener('change', (event) => {
        const fileList = event.target.files;
        handleFiles(fileList);
    });


    ddZone.addEventListener('dragover', (event) => event.preventDefault());
        const onDrop = async (event) => {
            event.preventDefault();

            // filesの初期化
            const files = [];

            // 最上階層から再起的に低い階層へファイルを取得するまで呼び出す
            const searchFile = async (entry) => {
            // ファイルのwebkitRelativePathにパスを登録する
            if (entry.isFile) {
                const file = await new Promise((resolve) => {
                    entry.file((file) => {
                    Object.defineProperty(file, "webkitRelativePath", {
                        // fullPathは/から始まるので二文字目から抜き出す
                        value: entry.fullPath.slice(1),
                    });
                    resolve(file);
                    });
                });
                files.push(file);
            // ファイルが現れるまでこちらの分岐をループし続ける
            } else if (entry.isDirectory) {
                const dirReader = entry.createReader();
                let allEntries = [];
                const getEntries = () =>
                    new Promise((resolve) => {
                        dirReader.readEntries((entries) => {
                            resolve(entries);
                        });
                    });
                    // readEntriesは100件ずつの取得なので、再帰で0件になるまで取ってくるようにする
                    // https://developer.mozilla.org/en-US/docs/Web/API/FileSystemDirectoryReader/readEntries
                    const readAllEntries = async () => {
                        const entries = await getEntries();
                        if (entries.length > 0) {
                            allEntries = [...allEntries, ...entries];
                            await readAllEntries();
                        }
                    };
                        await readAllEntries();
                    for (const entry of allEntries) {
                        await searchFile(entry);
                    }
            }
        };

        const items = event.dataTransfer.items;
        const calcFullPathPerItems = Array.from(items).map((item) => {
            return new Promise((resolve) => {
                const entry = item.webkitGetAsEntry();
                // nullの時は何もしない
                if (!entry) {
                    resolve;
                    return;
                }
                resolve(searchFile(entry));
                });
            });

            await Promise.all(calcFullPathPerItems);
            handleFiles(files);
        };

    ddZone.addEventListener('drop', onDrop);

    // ----------------------------------------------------
    // Here you can customize a pipeline of handlers for
    // inbound properties from the Streamlit client app
    // Simply log received data dictionary

  // Access values sent from Streamlit!
  function dataUpdate_Handler(props) {
    username_label.innerHTML = props.username
    collectionname_label.innerHTML = props.collectionname
    ACCESS_TOKEN = props.access_token
    collectionname_label.innerHTML = props.collectionname
  }

    function log_Handler(props) {
        //console.log("Received from Streamlit: " + JSON.stringify(props))
    };

    // パイプラインセット
    let pipeline = [log_Handler,dataUpdate_Handler];

    // パイプライン初期化
    initialize(pipeline);
