"use client";

import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import TWEEN from "@tweenjs/tween.js";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

export default function Home() {
  const mountRef = useRef(null);
  const cameraRef = useRef(null);
  const [scene, setScene] = useState(null);
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
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
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

    const axesHelper = new THREE.AxesHelper(5);
    scene.add(axesHelper);

    const cubeSize = 1;
    const spacing = 1.2;
    const cubesData = [];
    let number = 1;

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
        context.fillText(number.toString(), 64, 64);
      }
      return new THREE.CanvasTexture(canvas);
    };

    for (let x = 0; x < 5; x++) {
      for (let y = 0; y < 5; y++) {
        for (let z = 0; z < 5; z++) {
          const geometry = new THREE.BoxGeometry(cubeSize, cubeSize, cubeSize);
          const material = new THREE.MeshPhongMaterial({
            color: 0x00ff00,
            transparent: false, // Changed to false to remove translucency
          });

          const cube = new THREE.Mesh(geometry, material);
          const position = new THREE.Vector3(
            (x - 2) * spacing,
            (y - 2) * spacing,
            (z - 2) * spacing
          );
          cube.position.copy(position);

          // Create sprite for number (always faces camera)
          const numberTexture = createNumberTexture(number);
          const spriteMaterial = new THREE.SpriteMaterial({
            map: numberTexture,
            sizeAttenuation: false, // This makes the sprite size consistent regardless of distance
          });
          const sprite = new THREE.Sprite(spriteMaterial);
          sprite.scale.set(0.15, 0.15, 1); // Adjust size of number
          sprite.position.copy(position);

          // Add cube data with coordinates
          cubesData.push({
            number,
            position: position.clone(),
            mesh: cube,
            numberMesh: sprite,
            coordinates: { x, y, z },
          });

          scene.add(cube);
          scene.add(sprite);
          number++;
        }
      }
    }

    setCubes(cubesData);
    setScene(scene);

    const animate = () => {
      requestAnimationFrame(animate);
      controls.update();
      TWEEN.update();
      renderer.render(scene, camera);
    };
    animate();

    return () => {
      mountRef.current?.removeChild(renderer.domElement);
      renderer.dispose();
    };
  }, []);

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
    <main className="min-h-screen flex flex-row ">
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
