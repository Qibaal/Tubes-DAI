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
          const canvas = document.createElement("canvas");
          canvas.width = 128;
          canvas.height = 128;
          const context = canvas.getContext("2d");
          if (context) {
            context.fillStyle = "white";
            context.font = "bold 64px Arial";
            context.textAlign = "center";
            context.textBaseline = "middle";
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
  
  

  // Handle user input for cube positions
  const handlePositionChange = (e, cubeIndex) => {
    const { name, value } = e.target;
    setPositions((prev) => ({
      ...prev,
      [cubeIndex]: { ...prev[cubeIndex], [name]: value },
    }));
  };

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
    }
  };
  

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
    </main>
  );
}
