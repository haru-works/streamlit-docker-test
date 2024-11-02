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

    setFrameHeight(25);
  };

  function setFrameHeight(height) {
    _sendMessage(SET_FRAME_HEIGHT, { height: height })
  };

  // The `data` argument can be any JSON-serializable value.
  function notifyHost(data) {
    _sendMessage(SET_COMPONENT_VALUE, data)
  };

////////////////////////////////////////////////////////////////
    const test_label = document.getElementById("test_label")

    var ACCESS_TOKEN =null;
    
    const toBase64DataUri = file => new Promise(resolve => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.readAsDataURL(file);
      });

    // ----------------------------------------------------
    // Here you can customize a pipeline of handlers for
    // inbound properties from the Streamlit client app
    // Simply log received data dictionary



    
  // Access values sent from Streamlit!
  function dataUpdate_Handler(props) {
    test_label.innerHTML = props.test
  }

    function log_Handler(props) {
        console.log("Received from Streamlit: " + JSON.stringify(props))
    };

    // パイプラインセット
    let pipeline = [log_Handler,dataUpdate_Handler];

    // パイプライン初期化
    initialize(pipeline);
