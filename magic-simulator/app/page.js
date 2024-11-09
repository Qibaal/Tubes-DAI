"use client";
import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import TWEEN from "@tweenjs/tween.js";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

export default function Home() {
  const mountRef = useRef(null);
  const cameraRef = useRef(null); // Create a ref for the camera
  const [selectedCubes, setSelectedCubes] = useState([]);
  // const [scene, setScene] = useState(null);
  const [cubes, setCubes] = useState([]);
  const [positions, setPositions] = useState({
    first: { x: "", y: "", z: "" },
    second: { x: "", y: "", z: "" },
  });

  useEffect(() => {
    if (!mountRef.current) return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(
      75,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );
    cameraRef.current = camera; // Assign the camera to the ref
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    mountRef.current.appendChild(renderer.domElement);

    // Camera position
    camera.position.set(10, 10, 10);
    camera.lookAt(0, 0, 0);

    // Controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    // Create cubes
    const cubeSize = 1;
    const spacing = 1.2;
    const cubesData = [];
    let number = 1;

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

          // Add number as texture
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

          // Add cube data
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

    setCubes(cubesData);
    // setScene(scene);

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      controls.update();
      TWEEN.update();
      renderer.render(scene, camera);
    };
    animate();

    // Cleanup
    return () => {
      mountRef.current?.removeChild(renderer.domElement);
      renderer.dispose();
    };
  }, []);

  // const handleCubeClick = (event) => {
  //   if (!scene || !cameraRef.current) return;

  //   const raycaster = new THREE.Raycaster();
  //   const mouse = new THREE.Vector2(
  //     (event.clientX / window.innerWidth) * 2 - 1,
  //     -(event.clientY / window.innerHeight) * 2 + 1
  //   );

  //   raycaster.setFromCamera(mouse, cameraRef.current);
  //   const intersects = raycaster.intersectObjects(scene.children, true);

  //   if (intersects.length > 0) {
  //     const clickedCube = intersects[0].object;
  //     const cubeData = cubes.find((cube) => cube.mesh === clickedCube);

  //     if (cubeData) {
  //       setSelectedCubes((prev) => {
  //         if (prev.length === 2) return [cubeData.number];
  //         return [...prev, cubeData.number];
  //       });

  //       if (selectedCubes.length === 1) {
  //         // Animate cube switch
  //         const cube1 = cubes.find((c) => c.number === selectedCubes[0]);
  //         const cube2 = cubeData;

  //         if (cube1 && cube2.mesh && cube1.mesh) {
  //           const position1 = cube1.position.clone();
  //           const position2 = cube2.position.clone();

  //           new TWEEN.Tween(cube1.mesh.position)
  //             .to(position2, 1000)
  //             .easing(TWEEN.Easing.Quadratic.InOut)
  //             .start();

  //           new TWEEN.Tween(cube2.mesh.position)
  //             .to(position1, 1000)
  //             .easing(TWEEN.Easing.Quadratic.InOut)
  //             .start();

  //           // Update positions in state
  //           setCubes((prev) =>
  //             prev.map((c) => {
  //               if (c.number === cube1.number) {
  //                 return { ...c, position: position2 };
  //               }
  //               if (c.number === cube2.number) {
  //                 return { ...c, position: position1 };
  //               }
  //               return c;
  //             })
  //           );
  //         }
  //       }
  //     }
  //   }
  // };

  const handlePositionChange = (e, cubeIndex) => {
    const { name, value } = e.target;
    setPositions((prev) => ({
      ...prev,
      [cubeIndex]: { ...prev[cubeIndex], [name]: value },
    }));
  };

  const handlePositionSwap = () => {
    const { first, second } = positions;
    console.log(first)
    console.log(second)

    // Find cubes based on their positions
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

      // Animate the swap
      new TWEEN.Tween(firstCube.mesh.position)
        .to(pos2, 1000)
        .easing(TWEEN.Easing.Quadratic.InOut)
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

  // useEffect(() => {
  //   window.addEventListener("click", handleCubeClick);
  //   return () => window.removeEventListener("click", handleCubeClick);
  // }, [scene, selectedCubes]);

  return (
    <main className="min-h-screen flex flex-row ">
      {/* Description */}
      {/* Cube */}
      <section className="flex flex-col bg-gray-700">
        <div>
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

          <button onClick={handlePositionSwap}>Swap Cubes</button>
        </div>

        <div ref={mountRef} />
      </section>
    </main>
  );
}
