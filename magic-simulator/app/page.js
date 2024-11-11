"use client"; // This enables server-side rendering for the component

import { useEffect, useRef, useState } from "react"; // React hooks for state management and DOM references
import * as THREE from "three"; // Three.js library for 3D rendering
import TWEEN from "@tweenjs/tween.js"; // Library for animation tweening
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls"; // Module for mouse controls in Three.js

export default function Home() {
  // Create references for DOM element and camera
  const mountRef = useRef(null);
  const cameraRef = useRef(null);
  const [selectedCubes, setSelectedCubes] = useState([]); // State for storing selected cubes
  const [cubes, setCubes] = useState([]); // State for storing cube data
  const [positions, setPositions] = useState({ // State for storing user-input positions for swapping
    first: { x: "", y: "", z: "" },
    second: { x: "", y: "", z: "" },
  });

<<<<<<< Updated upstream
  useEffect(() => {
    if (!mountRef.current) return;
  
    // Initialize scene, camera, and renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(
      75, // Field of view
      window.innerWidth / window.innerHeight, // Aspect ratio
      0.1, // Near clipping plane
      1000 // Far clipping plane
    );
    cameraRef.current = camera; // Store the camera in the ref
  
    const renderer = new THREE.WebGLRenderer({ antialias: true }); // Renderer with anti-aliasing
    renderer.setSize(window.innerWidth, window.innerHeight); // Set renderer size
    mountRef.current.appendChild(renderer.domElement); // Append renderer to the DOM
  
    // Set initial camera position and orientation
    camera.position.set(10, 10, 10);
    camera.lookAt(0, 0, 0);
  
    // Enable orbit controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; // Enable damping for smoother controls
  
    // Add an AxesHelper to the scene
    const axesHelper = new THREE.AxesHelper(5); // Length of each axis line
    scene.add(axesHelper);
  
    // Variables for cube properties
    const cubeSize = 1;
    const spacing = 1.2;
    const blocksData = [];
    let number = 1; // Initial block value
  
    // Nested loop to create a 5x5x5 grid of cubes as 'blocks'
    for (let x = 0; x < 5; x++) {
      for (let y = 0; y < 5; y++) {
        for (let z = 0; z < 5; z++) {
          // Create cube geometry and material
          const geometry = new THREE.BoxGeometry(cubeSize, cubeSize, cubeSize);
          const material = new THREE.MeshPhongMaterial({
            color: 0x00ff00,
            transparent: true,
            opacity: 0.8,
          });
  
          const cube = new THREE.Mesh(geometry, material);
          const position = new THREE.Vector3(
            (x - 2) * spacing,
            (y - 2) * spacing,
            (z - 2) * spacing
          );
          cube.position.copy(position);
  
          // Create and apply texture with the block value
=======
  const [cost, setCost] = useState(initialConfig.initial_cost);
  const [finalConfig, setFinalConfig] = useState([]);
  const [currentCube, setCurrentCube] = useState(initialConfig.initial_cube);
  const [elapsedTime, setTime] = useState(0);

  const [iterations, setIterations] = useState(0);
  const [stuck, setStuck] = useState(0);

  const [geneticConfig, setGeneticConfig] = useState(0);

  const [sliderItr, setSlider] = useState(0);

  const updateConfig = (algoName) => {
    if (algoName === "initial_value") {
      setCost(initialConfig.initial_cost);
      setCurrentCube(initialConfig.initial_cube);
      setAlgo(algoName);
      return;
    }

    const selectedConfig = config.find(
      (c) => c.name.toLowerCase() === algoName
    );

    if (selectedConfig) {
      setTime(selectedConfig.time);
      setCost(selectedConfig.final_cost);
      setFinalConfig(selectedConfig.final_cube);

      // For simulated annealing
      if (selectedConfig.stuck_frequency) {
        setStuck(selectedConfig.stuck_frequency);
      }
    }
    setAlgo(algoName);
    setCurrentCube(selectedConfig.final_cube);
  };

  const handleToInitial = (stateType) => {
    setTime(0);
    setCost(initialConfig.initial_cost);
    setCurrentCube(initialConfig.initial_cube);
    setStuck(0);
  };

  const handleGeneticConfig = (state) => {
    setGeneticConfig(geneticConfig + state);
    if (geneticConfig < 0) setGeneticConfig(0);

    console.log(geneticConfig);
  };

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

const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
directionalLight.position.set(10, 10, 10);

  
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

  if (cubes.length === 0) {
    // Initialize cubes for the first time
    const cubeSize = 1.3;
    const spacing = 3;
    const cubesData = [];
    let numberIndex = 0;

    for (let x = 0; x < 5; x++) {
      for (let y = 0; y < 5; y++) {
        for (let z = 0; z < 5; z++) {
          const number = currentCube[numberIndex]; // Get value from the array
          const geometry = new THREE.BoxGeometry(cubeSize, cubeSize, cubeSize);
          const edgesGeometry = new THREE.EdgesGeometry(geometry);

          // Create material for the edges with lower opacity
          const edgesMaterial = new THREE.LineBasicMaterial({
            color: 0x00ff00,
            transparent: true,
            opacity: 0.35,
          });

          const edges = new THREE.LineSegments(edgesGeometry, edgesMaterial);
          edges.position.set((x - 2) * spacing, (y - 2) * spacing, (z - 2) * spacing);
          scene.add(edges);

          // Add value display as a canvas texture
>>>>>>> Stashed changes
          const canvas = document.createElement("canvas");
          canvas.width = 128;
          canvas.height = 128;
          const context = canvas.getContext("2d");
          if (context) {
            context.fillStyle = "white";
            context.font = "bold 64px Arial";
            context.textAlign = "center";
            context.textBaseline = "middle";
<<<<<<< Updated upstream
            context.fillText(number.toString(), 64, 64);
          }
  
          const texture = new THREE.CanvasTexture(canvas);
          const textMaterial = new THREE.MeshBasicMaterial({
            map: texture,
            transparent: true,
          });
  
          const textMesh = new THREE.Mesh(
            new THREE.PlaneGeometry(cubeSize * 0.8, cubeSize * 0.8),
            textMaterial
          );
          textMesh.position.z = cubeSize / 2 + 0.01;
          cube.add(textMesh);
  
          // Add block data with coordinates and blockValue
          const block = {
            xCor: (x - 2) * spacing,
            yCor: (y - 2) * spacing,
            zCor: (z - 2) * spacing,
            blockValue: number,
            mesh: cube, // Store the mesh for reference
          };
  
          blocksData.push(block);
          scene.add(cube); // Add the cube to the scene
          number++; // Increment block value
        }
      }
    }
  
    setCubes(blocksData); // Store generated blocks in state
  
    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      controls.update();
      TWEEN.update();
      renderer.render(scene, camera);
    };
    animate(); // Start animation loop
  
    // Cleanup function to remove renderer on component unmount
    return () => {
      mountRef.current?.removeChild(renderer.domElement);
      renderer.dispose(); // Dispose of renderer resources
    };
  }, []);
  
=======
            context.fillText(number, 64, 64);
          }
          const numberTexture = new THREE.CanvasTexture(canvas);
          const numberMaterial = new THREE.SpriteMaterial({ map: numberTexture });
          const numberSprite = new THREE.Sprite(numberMaterial);
          numberSprite.scale.set(0.5, 0.5, 1);
          numberSprite.position.set((x - 2) * spacing, (y - 2) * spacing, (z - 2) * spacing);
          scene.add(numberSprite);

          cubesData.push({
            blockValue: number,
            xCor: (x - 2) * spacing,
            yCor: (y - 2) * spacing,
            zCor: (z - 2) * spacing,
            mesh: edges,
            numberSprite: numberSprite,
          });

          numberIndex++;
        }
      }
    }

    setCubes(cubesData);
  } else {
    // Clear existing scene and re-add cubes with updated positions
    scene.clear();
    scene.add(ambientLight);
    scene.add(directionalLight);

    cubes.forEach((cube) => {
      scene.add(cube.mesh);

      // Remove existing sprite if present
      if (cube.numberSprite) {
        scene.remove(cube.numberSprite);
      }

      // Update value display as a canvas texture
      const canvas = document.createElement("canvas");
      canvas.width = 128;
      canvas.height = 128;
      const context = canvas.getContext("2d");
      if (context) {
        context.fillStyle = "white";
        context.font = "bold 64px Arial";
        context.textAlign = "center";
        context.textBaseline = "middle";
        context.fillText(cube.blockValue, 64, 64);
      }
      const numberTexture = new THREE.CanvasTexture(canvas);
      const numberMaterial = new THREE.SpriteMaterial({ map: numberTexture });
      cube.numberSprite = new THREE.Sprite(numberMaterial);
      cube.numberSprite.scale.set(0.5, 0.5, 1);
      cube.numberSprite.position.set(cube.xCor, cube.yCor, cube.zCor);

      // Add updated sprite to scene and update reference
      scene.add(cube.numberSprite);
    });
  }

  const animate = () => {
    requestAnimationFrame(animate);
    controls.update();
    TWEEN.update();  // Ensures TWEEN animations progress correctly
    renderer.render(scene, camera);
  };
  animate();


  return () => {
    mountRef.current?.removeChild(renderer.domElement);
    renderer.dispose();
  };
}, [cubes]);



>>>>>>> Stashed changes
  

  // Handle user input for cube positions
  const handlePositionChange = (e, cubeIndex) => {
    const { name, value } = e.target;
    setPositions((prev) => ({
      ...prev,
      [cubeIndex]: { ...prev[cubeIndex], [name]: value },
    }));
  };

<<<<<<< Updated upstream
  // Handle cube position swapping
  const handlePositionSwap = () => {
    const { first, second } = positions;
  
    // Parse the input coordinates and convert them from 1-based (1 to 5) to internal coordinate system
    const spacing = 1.2;
    const convertToInternal = (value) => (value - 3) * spacing; // Converts 1-5 range to -2.4 to 2.4 range
  
    const firstX = convertToInternal(parseInt(first.x, 10));
    const firstY = convertToInternal(parseInt(first.y, 10));
    const firstZ = convertToInternal(parseInt(first.z, 10));
    const secondX = convertToInternal(parseInt(second.x, 10));
    const secondY = convertToInternal(parseInt(second.y, 10));
    const secondZ = convertToInternal(parseInt(second.z, 10));
  
    // Find cubes based on their coordinates
    const firstCube = cubes.find(
      (c) =>
        c.xCor === firstX &&
        c.yCor === firstY &&
        c.zCor === firstZ
    );
  
    const secondCube = cubes.find(
      (c) =>
        c.xCor === secondX &&
        c.yCor === secondY &&
        c.zCor === secondZ
    );
  
    // Check if both cubes were found
    if (firstCube && secondCube) {
      const pos1 = firstCube.mesh.position.clone();
      const pos2 = secondCube.mesh.position.clone();
  
      // Swap blockValue between the two cubes
      const tempValue = firstCube.blockValue;
      firstCube.blockValue = secondCube.blockValue;
      secondCube.blockValue = tempValue;
  
      // Update the textures on the cubes to reflect the new values
      const updateCubeTexture = (cube) => {
        const canvas = document.createElement("canvas");
        canvas.width = 128;
        canvas.height = 128;
        const context = canvas.getContext("2d");
        if (context) {
          context.clearRect(0, 0, canvas.width, canvas.height); // Clear previous content
          context.fillStyle = "white";
          context.font = "bold 64px Arial";
          context.textAlign = "center";
          context.textBaseline = "middle";
          context.fillText(cube.blockValue.toString(), 64, 64);
        }
  
        const texture = new THREE.CanvasTexture(canvas);
        cube.mesh.children[0].material.map = texture; // Update texture map
        cube.mesh.children[0].material.needsUpdate = true; // Mark for update
      };
  
      updateCubeTexture(firstCube);
      updateCubeTexture(secondCube);
  
      // Animate the position swap
      new TWEEN.Tween(firstCube.mesh.position)
        .to(pos2, 1000) // 1-second duration
        .easing(TWEEN.Easing.Quadratic.InOut)
        .start();
  
      new TWEEN.Tween(secondCube.mesh.position)
        .to(pos1, 1000)
        .easing(TWEEN.Easing.Quadratic.InOut)
        .start();
  
      // Update the block positions in the state
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
  
      // Display success message
      window.alert("Block swap successful!");
    } else {
      // Display failure message
      window.alert("Block swap failed: One or both of the blocks could not be found. Check the input coordinates.");
=======
  const handlePositionSwap = (firstValue, secondValue) => {
    // Find the cubes to swap based on their block values
    const firstCube = cubes.find((c) => c.blockValue === firstValue);
    const secondCube = cubes.find((c) => c.blockValue === secondValue);

    if (firstCube && secondCube) {
        // Clone the current cubes array to avoid direct mutation
        const updatedCubes = cubes.map((cube) => {
            if (cube.blockValue === firstValue) {
                return { ...cube, xCor: secondCube.xCor, yCor: secondCube.yCor, zCor: secondCube.zCor };
            } else if (cube.blockValue === secondValue) {
                return { ...cube, xCor: firstCube.xCor, yCor: firstCube.yCor, zCor: firstCube.zCor };
            }
            return cube;
        });

        // Update positions and initiate TWEEN animations
        new TWEEN.Tween(firstCube.mesh.position)
            .to({ x: secondCube.xCor, y: secondCube.yCor, z: secondCube.zCor }, 1000)
            .easing(TWEEN.Easing.Quadratic.InOut)
            .start();

        new TWEEN.Tween(secondCube.mesh.position)
            .to({ x: firstCube.xCor, y: firstCube.yCor, z: firstCube.zCor }, 1000)
            .easing(TWEEN.Easing.Quadratic.InOut)
            .start();

        // Update the cubes state to reflect new coordinates
        setCubes(updatedCubes);
    } else {
        alert("Cube swap failed: One or both cube values not found.");
>>>>>>> Stashed changes
    }
};


  const reRenderScene = () => {
    scene.clear();
    scene.add(ambientLight);
    scene.add(directionalLight);
  
    cubes.forEach((cube) => {
      scene.add(cube.mesh);
  
      // Re-add value display as a canvas texture
      const canvas = document.createElement("canvas");
      canvas.width = 128;
      canvas.height = 128;
      const context = canvas.getContext("2d");
      if (context) {
        context.fillStyle = "white";
        context.font = "bold 64px Arial";
        context.textAlign = "center";
        context.textBaseline = "middle";
        context.fillText(cube.blockValue, 64, 64);
      }
      const numberTexture = new THREE.CanvasTexture(canvas);
      const numberMaterial = new THREE.SpriteMaterial({ map: numberTexture });
      const numberSprite = new THREE.Sprite(numberMaterial);
      numberSprite.scale.set(0.5, 0.5, 1);
      numberSprite.position.set(cube.xCor, cube.yCor, cube.zCor);
      scene.add(numberSprite);
    });
  };
  

const [firstValue, setFirstValue] = useState(null);
const [secondValue, setSecondValue] = useState(null);

  return (
    <main className="min-h-screen flex flex-row ">
      {/* User interface for position input and swap */}
      <section className="flex flex-col bg-gray-700">
        <div>
          {/* Input fields for the first cube's position */}
          <h3>First Cube Position</h3>
          <input
            type="number"
            name="x"
            placeholder="X"
            value={positions.first.x}
            onChange={(e) => handlePositionChange(e, "first")}
          />
          <input
            type="number"
            name="y"
            placeholder="Y"
            value={positions.first.y}
            onChange={(e) => handlePositionChange(e, "first")}
          />
          <input
            type="number"
            name="z"
            placeholder="Z"
            value={positions.first.z}
            onChange={(e) => handlePositionChange(e, "first")}
          />

          {/* Input fields for the second cube's position */}
          <h3>Second Cube Position</h3>
          <input
            type="number"
            name="x"
            placeholder="X"
            value={positions.second.x}
            onChange={(e) => handlePositionChange(e, "second")}
          />
          <input
            type="number"
            name="y"
            placeholder="Y"
            value={positions.second.y}
            onChange={(e) => handlePositionChange(e, "second")}
          />
          <input
            type="number"
            name="z"
            placeholder="Z"
            value={positions.second.z}
            onChange={(e) => handlePositionChange(e, "second")}
          />

          {/* Button to trigger the cube swap */}
          <button onClick={handlePositionSwap}>Swap Cubes</button>
        </div>

        <div ref={mountRef} /> {/* Container for 3D scene */}
      </section>
<<<<<<< Updated upstream
=======

      {/* Cube */}
      <div className="flex flex-row">
        <div className="flex flex-col items-center px-6 py-4 w-1/4 space-y-8 bg-gray-500">
          <h2 className="text-white font-bold text-xl">{algo.toUpperCase()}</h2>

          <input
            type="number"
            placeholder="First Cube Value"
            className="p-2 rounded border border-gray-300"
            onChange={(e) => setFirstValue(parseInt(e.target.value, 10))}
          />
          <input
            type="number"
            placeholder="Second Cube Value"
            className="p-2 rounded border border-gray-300"
            onChange={(e) => setSecondValue(parseInt(e.target.value, 10))}
          />
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded"
            onClick={() => {
              if (isNaN(firstValue) || isNaN(secondValue)) {
                alert("Please enter valid cube values for both inputs.");
                return;
              }
              handlePositionSwap(firstValue, secondValue);
            }}
          >
            Swap Cubes
          </button>


          {algo != "initial_value" && (
            <div className="w-full flex flex-col space-y-8 items-center">
              <div className="w-full flex flex-col space-y-8 bg-white text-black rounded-xl pt-4 pb-8 px-4 ">
                <p>
                  Slider Value: <span className="font-bold">{sliderItr}</span>
                </p>
                <DraggableSlider
                  min={sliderItr}
                  max={5000}
                  initialValue={0}
                  onChange={(newValue) => setSlider(newValue)}
                />
              </div>

              <div className="w-full bg-white text-black rounded-xl py-4 px-4">
                <p>Current Cost</p>
                <p className="font-bold">8000</p>
                <br />
                <p>First Index Switched (Value)</p>
                <p className="font-bold">3, 1, 2 (114)</p>
                <br />
                <p>Second Index Switched</p>
                <p className="font-bold">0, 0, 0 (2)</p>
              </div>

              <Link href="#viz" className="w-full">
                <button className="font-bold bg-white w-full py-2 rounded-lg">See Graph</button>
              </Link>
            </div>
          )}
        </div>

        <div ref={mountRef} className="w-3/4" />
      </div>

      {/* Viz */}
      <div
        className="w-full bg-white min-h-screen flex flex-col items-center justify-center"
        id="viz"
      >
        <h2>Visualization</h2>
        <Image src={VizMock} alt="viz-mock" />
        <button>
          <a href="#cube">Back to Cube</a>
        </button>
      </div>
>>>>>>> Stashed changes
    </main>
  );
}
