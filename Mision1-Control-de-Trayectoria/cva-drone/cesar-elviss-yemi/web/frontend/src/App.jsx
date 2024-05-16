/* import video from './assets/video.mp4' */
import { useEffect, useRef } from 'react';
import app from './styles/app.module.css';
import header from './styles/header.module.css';

function App() {
  const videoRef = useRef(null)

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:3000');
    ws.binaryType = 'arraybuffer';

    ws.onopen = () => {
      console.log('Conexión establecida');
    }

    /* const mediaSource = new MediaSource();
    let mediaSourceOpen = false;
    let mediaSourceBuffer;

    videoRef.current.src = URL.createObjectURL(mediaSource);

    mediaSource.addEventListener('sourceopen', () => {
      mediaSourceOpen = true;
      mediaSourceBuffer = mediaSource.addSourceBuffer('video/mp4; codecs="avc1.42E01E, mp4a.40.2"');
    }); */

    /* checa si el video lleva algo y muestralo en consola */
    /* mediaSource.addEventListener('sourceclose', () => {
      console.log('Video terminado');
    }); */

    ws.onmessage = (event) => {
      const data = new Uint8Array(event.data);
      mediaSourceBuffer.appendBuffer(data);
    };

    ws.onmessage = (msg) => {
      const data = new Uint8Array(msg.data);
      const blob = new Blob([data], { type: 'video/mp4' });
      const url = URL.createObjectURL(blob);
      videoRef.current.src = url;
    }

    /* ws.onmessage = (event) => {
      const blob = new Blob([event.data], { type: 'image/jpeg' });
      const url = URL.createObjectURL(blob);
      videoRef.current.src = url;
    };

    ws.onmessage = (event) => {
      // Verifica si los datos recibidos son datos de imagen válidos
      if (event.data instanceof Blob) {
        // Crea una URL a partir del Blob y asígnala al atributo src del elemento img
        videoRef.current.src = URL.createObjectURL(event.data);
      } else {
        console.error('Los datos recibidos no son un Blob válido de imagen');
      }
    }; */

    ws.onclose = () => {
      console.log('Conexión cerrada');
    }

    return () => {
      ws.close();
    }
  }, []);


  return (
    <>
      <div className={app.container}>
        <header className={header.header}>
          <h1 className={header.h1}>Mixtli <span className={header.span}>drone vision</span></h1>
        </header>
        <main className={app.main}>
          {/* <video className={app.video} autoPlay loop muted>
            <source src={videoRef} type="video/mp4" />
            Your browser does not support the video tag.
          </video> */}
          <video ref={videoRef} autoPlay controls width="640" height="360" />
          <img ref={videoRef} alt="Tello Stream" />
          <aside className={app.aside}>
            <div className={app.controls}>
              <h2 className={app.h2}>Controls</h2>
              <div className={app.controlsContainer}>
              </div>
            </div>
            <div className={app.statics}>
              <h2 className={app.h2}>Statics</h2>
              <div className={app.staticsContainer}>
              </div>
            </div>
          </aside>
        </main>
        <footer className={app.footer}>
          <p className={app.p}>Built by <a href="https://www.instagram.com/tecmixtli/" target="_blank" rel="noreferrer">TechMixtli</a></p>
        </footer>
      </div>
    </>
  )
}

export default App
