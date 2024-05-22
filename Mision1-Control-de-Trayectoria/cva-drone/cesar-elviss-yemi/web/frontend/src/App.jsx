import React, { useEffect, useState } from 'react';
import { HiMiniSignalSlash } from "react-icons/hi2";
import circle from './assets/circle.png';
import pentagon from './assets/pentagon.png';
import rombo from './assets/rombo.png';
import square from './assets/square.png';
import triangle from './assets/triangle.png';
import app from './styles/app.module.css';
import header from './styles/header.module.css';

function App() {
  const [imageSrc, setImageSrc] = useState('');
  const [squares, setSquares] = useState(0);
  const [pentagons, setPentagons] = useState(0);
  const [rombos, setRombos] = useState(0);
  const [triangles, setTriangles] = useState(0);
  const [circles, setCircles] = useState(0);
  const [hello, setHello] = useState(0)

  /* const [figures, setFigures] = useState({
    squares: 0,
    pentagons: 0,
    rombos: 0,
    triangles: 0,
    circles: 0,
  }); */

  useEffect(() => {
    const fetchHello = async () => {
      try {
        const response = await fetch('http://localhost:5003/squares');
        const data = await response.json();
        setHello(data.message)
        console.log(data);
      } catch (error) {
        console.error(error);
      }
    };
    fetchHello();

    const interval = setInterval(() => {
      fetchHello();
    }, 1000);

    return () => {
      clearInterval(interval);
    }
  }, []);

  useEffect(() => {
    const fetchSquares = async () => {
      try {
        const response = await fetch('http://localhost:5001/squares');
        const data = await response.json();
        setSquares(data.message);
        console.log(data);
      } catch (error) {
        console.error(error);
      }
    };
    fetchSquares();

    const interval = setInterval(() => {
      fetchSquares();
    }, 1000);

    return () => {
      clearInterval(interval);
    }
  }, []);

  useEffect(() => {
    const fetchPentagons = async () => {
      try {
        const response = await fetch('http://localhost:5001/pentagons');
        const data = await response.json();
        setPentagons(data.message);
        console.log(data);
      } catch (error) {
        console.error(error);
      }
    };
    fetchPentagons();

    const interval = setInterval(() => {
      fetchPentagons();
    }, 1000);

    return () => {
      clearInterval(interval);
    }
  }, []);

  useEffect(() => {
    const fetchRombos = async () => {
      try {
        const response = await fetch('http://localhost:5001/rombos');
        const data = await response.json();
        setRombos(data.message);
        console.log(data);
      } catch (error) {
        console.error(error);
      }
    };
    fetchRombos();

    const interval = setInterval(() => {
      fetchRombos();
    }, 1000);

    return () => {
      clearInterval(interval);
    }
  }, []);

  useEffect(() => {
    const fetchTriangles = async () => {
      try {
        const response = await fetch('http://localhost:5001/triangles');
        const data = await response.json();
        setTriangles(data.message);
        console.log(data);
      } catch (error) {
        console.error(error);
      }
    };
    fetchTriangles();

    const interval = setInterval(() => {
      fetchTriangles();
    }, 1000);

    return () => {
      clearInterval(interval);
    }
  }, []);

  useEffect(() => {
    const fetchCircles = async () => {
      try {
        const response = await fetch('http://localhost:5001/circles');
        const data = await response.json();
        setCircles(data.message);
        console.log(data);
      } catch (error) {
        console.error(error);
      }
    };
    fetchCircles();

    const interval = setInterval(() => {
      fetchCircles();
    }, 1000);

    return () => {
      clearInterval(interval);
    }
  }, []);

  const takeOff = async () => {
    try {
      const response = await fetch('http://localhost:5001/takeoff', {
        method: 'POST',
      });
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error(error);
    }
  };

  const land = async () => {
    try {
      const response = await fetch('http://localhost:5001/land', {
        method: 'POST',
      });
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8765');

    ws.onopen = () => {
      console.log('Conexión establecida');
    };

    ws.onmessage = (event) => {
      const base64Image = event.data;
      setImageSrc(`data:image/jpeg;base64,${base64Image}`);
    };

    ws.onclose = () => {
      console.log('Conexión cerrada');
    };

    return () => {
      ws.close();
    };
  }, []);

  return (
    <div className={app.container}>
      <header className={header.header}>
        <h1 className={header.h1}>Mixtli <span className={header.span}>drone vision</span></h1>
      </header>
      <main className={app.main}>
        {
          imageSrc ? (
            <img src={imageSrc} alt="Drone Stream" className={app.img} />
          ) : (
            <div className={app.blurryBackground}>
              <div className={app.bg}><span className={app.span}>No video streaming</span><HiMiniSignalSlash className={app.icon} /></div>
            </div>
          )
        }
        <aside className={app.aside}>
          <div className={app.controls}>
            <h2 className={app.h2}>Controls</h2>
            <div className={app.controlsContainer}>
              <button className={app.button} onClick={takeOff}>Take off</button>
              <button className={app.button} onClick={land}>Land</button>
              <span>{hello}</span>
              <span>squares: {squares}</span>
            </div>
          </div>
          <div className={app.statics}>
            <h2 className={app.h2}>Statics</h2>
            <div className={app.staticsContainer}>
              <figure>
                <img src={pentagon} alt="pentagon" className={app.img} />
                <figcaption className={app.figcaption}>{pentagons}</figcaption>
              </figure>

              <figure>
                <img src={rombo} alt="rombo" className={app.img} />
                <figcaption className={app.figcaption}>{rombos}</figcaption>
              </figure>

              <figure>
                <img src={triangle} alt="triangle" className={app.img} />
                <figcaption className={app.figcaption}>{triangles}</figcaption>
              </figure>

              <figure>
                <img src={circle} alt="circle" className={app.img} />
                <figcaption className={app.figcaption}>{circles}</figcaption>
              </figure>

              <figure>
                <img src={square} alt="square" className={app.img} />
                <figcaption className={app.figcaption}>{squares}</figcaption>
              </figure>

              {/* <figcaption className={app.figcaption}>Battery</figcaption>
                <progress className={app.progress} value="100" max="100"></progress> */}

              {/* <span className={app.p}>Battery: 100%</span>
              <span className={app.p}>Altitude: 0m</span>
              <span className={app.p}>Speed: 0km/h</span> */}
            </div>
          </div>
        </aside>
      </main>
      <footer className={app.footer}>
        <p className={app.p}>Built by <a href="https://www.instagram.com/tecmixtli/" target="_blank" rel="noreferrer">TechMixtli</a></p>
      </footer>
    </div>
  );
}

export default App;
