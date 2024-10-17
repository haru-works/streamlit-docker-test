
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

    window.parent.postMessage(outboundData, "*");
  };

  function initialize(pipeline) {
    window.addEventListener("message", (event) => {
      if (event.data.type == RENDER) {
        pipeline.forEach(handler => {
          handler(event.data.args)
        })
      }
    });

    _sendMessage(COMPONENT_READY, { apiVersion: 1 });

    setFrameHeight(100);
  };

  function setFrameHeight(height) {
    _sendMessage(SET_FRAME_HEIGHT, { height: height })
  };

  function notifyHost(data) {
    _sendMessage(SET_COMPONENT_VALUE, data)
  };

  const ddlink = document.getElementById('ddlink');
  var DOWNLOAD_FILE_API =null;
  var ACCESS_TOKEN =null;
  var user_name =null;
  var collection_name =null;
  var file_name =null;

  ddlink.addEventListener('click', () => {

    const param = "?username=" + user_name + "&collectionname=" + collection_name + "&filename=" + file_name
    const DL_URL = DOWNLOAD_FILE_API + param
    const requestOptions={
        method:"GET",
        mode:"cors",
        headers: {
            'Access-Control-Allow-Origin':'*',
            'Authorization': 'Bearer '+ ACCESS_TOKEN,
            'Accept': 'application/json',   
        },
    }

    fetch(DL_URL, requestOptions)
      .then(async res => (
        {
          filename: file_name,
          blob: await res.blob()
        }
      ))
      .then(resObj => {

          //console.log(resObj.res)

          // It is necessary to create a new blob object with mime-type explicitly set for all browsers except Chrome, but it works for Chrome too.
          const newBlob = new Blob([resObj.blob], { type: 'application/pdf' });
  
          // MS Edge and IE don't allow using a blob object directly as link href, instead it is necessary to use msSaveOrOpenBlob
          if (window.navigator && window.navigator.msSaveOrOpenBlob) {
              window.navigator.msSaveOrOpenBlob(newBlob);
          } else {
              // For other browsers: create a link pointing to the ObjectURL containing the blob.
              const objUrl = window.URL.createObjectURL(newBlob);
  
              let link = document.createElement('a');
              link.href = objUrl;
              link.download = resObj.filename;
              link.click()

              // For Firefox it is necessary to delay revoking the ObjectURL.
              setTimeout(() => { window.URL.revokeObjectURL(objUrl); }, 250);
          }
      })
      .catch((error) => {
          console.log('DOWNLOAD ERROR', error);
      });    
    notifyHost({
        value: "ok",
        dataType: "json",
    });
  });
    
  function dataUpdate_Handler(props) {
    ACCESS_TOKEN = props.access_token
    DOWNLOAD_FILE_API = props.download_file_api
    user_name = props.user_name
    collection_name = props.collection_name
    file_name = props.file_name
    ddlink.innerHTML = file_name
  }

  function log_Handler(props) {
      console.log("Received from Streamlit: " + JSON.stringify(props))
  };

  // パイプラインセット
  let pipeline = [log_Handler,dataUpdate_Handler];

  // パイプライン初期化
  initialize(pipeline);
