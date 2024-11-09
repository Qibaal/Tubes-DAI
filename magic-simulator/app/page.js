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
    const cubesData = [];
    let number = 1;
  
    // Nested loop to create a 5x5x5 grid of cubes
    for (let x = 0; x < 5; x++) {
      for (let y = 0; y < 5; y++) {
        for (let z = 0; z < 5; z++) {
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
  
          // Create and apply texture with the cube number
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
  
          cubesData.push({
            number,
            position: position.clone(),
            mesh: cube,
          });
          scene.add(cube);
          number++;
        }
      }
    }
  
    setCubes(cubesData); // Store generated cubes in state
  
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
    console.log(first);
    console.log(second);

    // Find cubes based on provided positions
    const firstCube = cubes.find(
      (c) =>
        c.position.x === parseFloat(first.x) &&
        c.position.y === parseFloat(first.y) &&
        c.position.z === parseFloat(first.z)
    );

    const secondCube = cubes.find(
      (c) =>
        c.position.x === parseFloat(second.x) &&
        c.position.y === parseFloat(second.y) &&
        c.position.z === parseFloat(second.z)
    );

    if (firstCube && secondCube) {
      const pos1 = firstCube.position.clone();
      const pos2 = secondCube.position.clone();

      // Animate position swap between two cubes
      new TWEEN.Tween(firstCube.mesh.position)
        .to(pos2, 1000) // Duration of 1 second
        .easing(TWEEN.Easing.Quadratic.InOut) // Easing function for smooth animation
        .start();

      new TWEEN.Tween(secondCube.mesh.position)
        .to(pos1, 1000)
        .easing(TWEEN.Easing.Quadratic.InOut)
        .start();

      // Update state with new positions
      setCubes((prev) =>
        prev.map((c) => {
          if (c === firstCube) {
            return { ...c, position: pos2 };
          }
          if (c === secondCube) {
            return { ...c, position: pos1 };
          }
          return c;
        })
      );
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
