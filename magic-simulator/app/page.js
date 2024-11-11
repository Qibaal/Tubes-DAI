"use client";
import Image from "next/image";
import Link from "next/link";

import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import TWEEN from "@tweenjs/tween.js";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

import { initialConfig, config } from "./data/configData";
import DraggableSlider from "./components/DraggableSlider";

import VizMock from "@/public/graphs/bar-graph.png";
import Viz1 from "@/public/graphs/sac.png";
import Viz2 from "@/public/graphs/stochastic.jpg";
// import Viz3 from "@/public/graphs/sideways.png";
// import Viz4 from "@/public/graphs/rr.png";
// import Viz5 from "@/public/graphs/sa.png";
import Viz6 from "@/public/graphs/genetic.png";

import LeftTri from "@/public/left-arrow.png";
import RightTri from "@/public/right-arrow.png";
import PauseBut from "@/public/pause.png";

export default function Home() {
  const mountRef = useRef(null);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );

  const [algo, setAlgo] = useState("initial_value");

  const [cubes, setCubes] = useState([]);
  const [positions, setPositions] = useState({
    first: { x: "", y: "", z: "" },
    second: { x: "", y: "", z: "" },
  });

  const [cost, setCost] = useState(initialConfig.initial_cost);
  const [finalConfig, setFinalConfig] = useState([]);
  const [currentCube, setCurrentCube] = useState(initialConfig.initial_cube);
  const [currentSteps, setSteps] = useState([]);
  const [elapsedTime, setTime] = useState(0);

  const [run, setRun] = useState(1); // untuk opsi run keberapa

  const [stuck, setStuck] = useState(0); // stuck pada sideways
  const [geneticConfig, setGeneticConfig] = useState(0); // konfigurasi genetic

  const [sliderItr, setSlider] = useState(0); // slider use

  // Video Player
  const [play, setPlay] = useState(false);
  const [speed, setSpeed] = useState(1);

  const createNumberTexture = (number) => {
    const canvas = document.createElement("canvas");
    canvas.width = 128;
    canvas.height = 128;
    const context = canvas.getContext("2d");
    if (context) {
      context.fillStyle = "white";
      context.font = "bold 64px Arial";
      context.textAlign = "center";
      context.textBaseline = "middle";
      context.fillText(number, 64, 64);
    }
    return new THREE.CanvasTexture(canvas);
  };

  // CUBE RENDERING LOGICS
  useEffect(() => {
    if (!mountRef.current) return;

    const renderer = new THREE.WebGLRenderer({ antialias: true });

    renderer.setSize(window.innerWidth / 1.335, window.innerHeight / 1.335);
    mountRef.current.appendChild(renderer.domElement);

    // Camera position
    camera.position.set(10, 10, 10);
    camera.lookAt(0, 0, 0);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
    directionalLight.position.set(10, 10, 10);
    scene.add(directionalLight);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    const cubeSize = 1.3;
    const spacing = 3;
    const cubesData = [];
    let number = 1;
    let numberIndex = 0;

    for (let x = 0; x < 5; x++) {
      for (let y = 0; y < 5; y++) {
        for (let z = 0; z < 5; z++) {
          const geometry = new THREE.BoxGeometry(cubeSize, cubeSize, cubeSize);
          const edgesGeometry = new THREE.EdgesGeometry(geometry);

          // Create material for the edges with lower opacity
          const edgesMaterial = new THREE.LineBasicMaterial({
            color: 0x00ff00, // Green color for the outline
            transparent: true, // Enable transparency
            opacity: 0.35, // Set the opacity (0 is fully transparent, 1 is fully opaque)
          });

          // Create the edges mesh and add it to the scene
          const edges = new THREE.LineSegments(edgesGeometry, edgesMaterial);
          edges.position.set(
            (x - 2) * spacing,
            (y - 2) * spacing,
            (z - 2) * spacing
          );
          scene.add(edges);

          // Create and position the number sprite
          const number = currentCube[numberIndex];
          const numberTexture = createNumberTexture(number);
          const spriteMaterial = new THREE.SpriteMaterial({
            map: numberTexture,
            sizeAttenuation: false,
          });
          const sprite = new THREE.Sprite(spriteMaterial);
          sprite.scale.set(0.15, 0.15, 1);
          sprite.position.set(
            (x - 2) * spacing,
            (y - 2) * spacing,
            (z - 2) * spacing
          );

          scene.add(sprite);
          numberIndex++;
        }
      }
    }

    setCubes(cubesData);

    const animate = () => {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    return () => {
      mountRef.current?.removeChild(renderer.domElement);
      renderer.dispose();
    };
  }, [currentCube]);


  // LOGIC FOR ALGO SELECTION
  const updateAlgo = (algoName, runVal) => {
    if (algoName === "initial_value") {
      setCost(initialConfig.initial_cost);
      setCurrentCube(initialConfig.initial_cube);
      setAlgo(algoName);
      return;
    }

    const selectedConfig = config.find(
      (c) => c.name.toLowerCase() == algoName && c.run == runVal
    );

    if (selectedConfig) {
      setTime(selectedConfig.time);
      setCost(selectedConfig.final_cost);
      console.log(selectedConfig.final_cost)
      setFinalConfig(selectedConfig.final_cube);
      setSteps(selectedConfig.steps);

      // For simulated annealing
      if (selectedConfig.stuck_frequency) {
        setStuck(selectedConfig.stuck_frequency);
      }
    }
    setAlgo(algoName);

    // Set the current cube to the corresponding algo
    setCurrentCube(selectedConfig.final_cube);
  };

  const handleGeneticConfig = (runVal) => {
    if (runVal < 1) 
      return;
    else {
      console.log(algo)
      console.log(runVal)
      updateAlgo(algo, runVal)
    }
    console.log(runVal)
    setRun(runVal)
  }

  // LOGIC for VIDEO PLAYER
  const togglePlay = (newPlayState) => {
    setPlay(newPlayState);
  };

  const updateSpeed = (newSpeed) => {
    setSpeed(Number(newSpeed));
  };

  const handleSlide = (newValue) => {
    setSlider(newValue);
  };

  useEffect(() => {
    let interval;

    if (play) {
      interval = setInterval(() => {
        setSlider((prevSlider) => {
          if (prevSlider < currentSteps.length - 1) {
            return prevSlider + 1;
          } else {
            clearInterval(interval);
            setPlay(false); // Stop when the slider reaches the end
            return prevSlider;
          }
        });
      }, 1000 / speed); // Adjust interval timing based on speed
    } else {
      clearInterval(interval);
    }

    return () => clearInterval(interval);
  }, [play, speed]);

  // LOGIC FOR SWAP
  const handlePositionChange = (e, cubeIndex) => {
    const { name, value } = e.target;
    setPositions((prev) => ({
      ...prev,
      [cubeIndex]: { ...prev[cubeIndex], [name]: value },
    }));
  };

  const handlePositionSwap = () => {
    const { first, second } = positions;

    const spacing = 1.2;
    const convertToInternal = (value) => (value - 3) * spacing;

    const firstX = convertToInternal(parseInt(first.x, 10));
    const firstY = convertToInternal(parseInt(first.y, 10));
    const firstZ = convertToInternal(parseInt(first.z, 10));
    const secondX = convertToInternal(parseInt(second.x, 10));
    const secondY = convertToInternal(parseInt(second.y, 10));
    const secondZ = convertToInternal(parseInt(second.z, 10));

    const firstCube = cubes.find(
      (c) => c.xCor === firstX && c.yCor === firstY && c.zCor === firstZ
    );

    const secondCube = cubes.find(
      (c) => c.xCor === secondX && c.yCor === secondY && c.zCor === secondZ
    );

    if (firstCube && secondCube) {
      const pos1 = firstCube.mesh.position.clone();
      const pos2 = secondCube.mesh.position.clone();

      const tempValue = firstCube.blockValue;
      firstCube.blockValue = secondCube.blockValue;
      secondCube.blockValue = tempValue;

      const updateCubeTexture = (cube) => {
        const canvas = document.createElement("canvas");
        canvas.width = 128;
        canvas.height = 128;
        const context = canvas.getContext("2d");
        if (context) {
          context.clearRect(0, 0, canvas.width, canvas.height);
          context.fillStyle = "white";
          context.font = "bold 64px Arial";
          context.textAlign = "center";
          context.textBaseline = "middle";
          context.fillText(cube.blockValue.toString(), 64, 64);
        }

        const texture = new THREE.CanvasTexture(canvas);
        cube.mesh.children[0].material.map = texture;
        cube.mesh.children[0].material.needsUpdate = true;
      };

      updateCubeTexture(firstCube);
      updateCubeTexture(secondCube);

      new TWEEN.Tween(firstCube.mesh.position)
        .to(pos2, 1000)
        .easing(TWEEN.Easing.Quadratic.InOut)
        .start();

      new TWEEN.Tween(secondCube.mesh.position)
        .to(pos1, 1000)
        .easing(TWEEN.Easing.Quadratic.InOut)
        .start();

      setCubes((prev) =>
        prev.map((c) => {
          if (c === firstCube) {
            return { ...c, xCor: secondX, yCor: secondY, zCor: secondZ };
          }
          if (c === secondCube) {
            return { ...c, xCor: firstX, yCor: firstY, zCor: firstZ };
          }
          return c;
        })
      );
    }
  };

  return (
    <main className="min-h-screen flex flex-col bg-gray-400">
      <section className="flex flex-row justify-between py-4 px-6" id="cube">
        {/* Algo Picking */}
        <div className="flex flex-row items-center justify-center gap-8">
          <div>
            <select
              id="algorithms"
              name="algorithm_list"
              form="algorithm_form"
              value={algo}
              onChange={(e) => updateAlgo(e.target.value, run)}
              className="bg-white font-bold py-2 px-4 rounded-lg"
            >
              <option value="initial_value">Initial Config</option>
              <option value="steepest_ascent">Steepest Ascent</option>
              <option value="stochastic">Stochastic</option>
              <option value="sideways_move">Sideways Move</option>
              <option value="random_restart">Random Restart</option>
              <option value="simulated_annealing">Simulated Annealing</option>
              <option value="genetic">Genetic</option>
            </select>
          </div>

          {algo != "initial_value" && algo != "genetic" && (
            <div>
              <select
                id="cuberun"
                name="cuberun_list"
                form="cuberun_form"
                value={run}
                onChange={(e) =>{setRun(e.target.value); updateAlgo(algo, e.target.value)}}
                className="bg-white font-bold py-2 px-4 rounded-lg"
              >
                <option value={1}>First Run</option>
                <option value={2}>Second Run</option>
                <option value={3}>Third Run</option>
              </select>
            </div>
          )}

          {algo == "genetic" && (
            <div className="flex flex-row items-center justify-center gap-2">
              <Image
                src={LeftTri}
                alt="left triangle"
                onClick={() => handleGeneticConfig(run-1)}
              />
              <div className="flex flex-col text-center">
                <p>Populasi, Iterasi</p>
                <p>{run}, 1000</p>
              </div>
              <Image
                src={RightTri}
                alt="right triangle"
                onClick={() => handleGeneticConfig(run + 1)}
              />
            </div>
          )}
        </div>

        {/* Information */}
        {/* <div className="flex flex-row gap-4">
          <div>
            <p>Initial Cost</p>
            <p>{initialConfig.initial_cost}</p>
          </div>
          <div>
            <p>Best Cost</p>
            <p>{cost}</p>
          </div>
          <div>
            <p>Total time</p>
            <p>{elapsedTime}</p>
          </div>
          {algo == "steepest_ascent" ||
            algo == "stochastic" ||
            (algo == "sideways_move" && (
              <div>
                <p>Iterations</p>
                <p>{iterations}</p>
              </div>
            ))}
          {algo == "sideways_move" && (
            <div>
              <p>Maximum Sideways</p>
              <p>1000</p>
            </div>
          )}
          {algo == "random_restart" && (
            <>
              <div>
                <p>Restarts</p>
                <p>10</p>
              </div>
              <div>
                <p>Iteration per Restart</p>
                <p>1000</p>
              </div>
            </>
          )}
          {algo == "simulated_annealing" && (
            <div>
              <p>Stuck Frequency</p>
              <p>{elapsedTime}</p>
            </div>
          )}
        </div> */}
      </section>

      {/* Cube */}
      <div className="flex flex-row">
        <div className="flex flex-col items-center px-6 py-4 w-1/4 space-y-8 bg-gray-500">
          <h2 className="text-white font-bold text-xl">
            {algo.toUpperCase()}
            {algo != "initial_value" && algo != "genetic" && (
              <span>
                - {" "}
                {run == 1 && "First Run"}
                {run == 2 && "Second Run"}
                {run == 3 && "Third Run"}
              </span>
            )}
          </h2>

          {algo != "initial_value" && (
            <div className="w-full flex flex-col space-y-8 items-center">
              <div className="flex flex-row w-full space-x-4 ">
                {!play && (
                  <div
                    onClick={() => togglePlay(!play)}
                    className="flex flex-row items-center justify-center space-x-4 bg-white py-2 rounded-lg w-1/2"
                  >
                    <Image src={RightTri} alt="play-button" />
                    <p className="font-bold">Play</p>
                  </div>
                )}
                {play && (
                  <div
                    onClick={() => togglePlay(!play)}
                    className="flex flex-row items-center justify-center space-x-4 bg-white py-2 rounded-lg w-1/2"
                  >
                    <Image src={PauseBut} alt="pause-button" width={32} />
                    <p className="font-bold">Pause</p>
                  </div>
                )}
                <select
                  id="speed"
                  name="speed_list"
                  form="speed_form"
                  value={speed}
                  onChange={(e) => updateSpeed(e.target.value)}
                  className="bg-white w-1/2 font-bold"
                >
                  <option value={1}>1X</option>
                  <option value={2}>2X</option>
                  <option value={4}>4X</option>
                </select>
              </div>

              <div className="w-full flex flex-col space-y-8 bg-white text-black rounded-xl pt-4 pb-8 px-4 ">
                <p>
                  Iteration: <span className="font-bold">{sliderItr + 1}</span>
                </p>
                <DraggableSlider
                  min={0}
                  max={currentSteps.length - 1}
                  initialValue={0}
                  onChange={(newValue) => handleSlide(newValue)}
                />
              </div>

              <div className="w-full bg-white text-black rounded-xl py-4 px-4">
                <p>Current Cost</p>
                <p className="font-bold">{currentSteps[sliderItr].cost}</p>
                <br />
                <p>First Index Switched</p>
                <p className="font-bold">{currentSteps[sliderItr].index1}</p>
                <br />
                <p>Second Index Switched</p>
                <p className="font-bold">{currentSteps[sliderItr].index2}</p>
              </div>

              <Link href="#viz" className="w-full">
                <button className="font-bold bg-white w-full py-2 rounded-lg">
                  See Graph
                </button>
              </Link>
            </div>
          )}
        </div>

        <div ref={mountRef} className="w-3/4 h-full" />
      </div>

      {/* Viz */}
      <div
        className="w-full bg-white min-h-screen flex flex-col items-center space-y-32 py-32"
        id="viz"
      >
        <h2 className="font-bold text-5xl">Visualization</h2>
        {algo == "initial_value" && (
          <Image src={VizMock} alt="viz-mock" width={800} />
        )}
        {algo == "steepest_ascent" && (
          <Image src={Viz1} alt="viz-mock" width={800} />
        )}
        {algo == "stochastic" && (
          <Image src={Viz2} alt="viz-mock" width={800} />
        )}
        {/* { algo == "sideways_move" &&
          <Image src={Viz3} alt="viz-mock" width={800} /> 
        }
        { algo == "random_restart" &&
          <Image src={Viz4} alt="viz-mock" width={800}/> 
        }
        { algo == "simulated_annealing" &&
          <Image src={Viz5} alt="viz-mock" width={800}/> 
        } */}
        {algo == "genetic" && <Image src={Viz6} alt="viz-mock" width={800} />}
        <button className="bg-gray-300 px-16 py-4 rounded-xl">
          <a href="#cube" className="font-bold text-2xl">
            Back to Cube
          </a>
        </button>
      </div>
    </main>
  );
}
