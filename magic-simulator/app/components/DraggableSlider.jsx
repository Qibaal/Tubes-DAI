"use client"
import { useState, useRef, useEffect } from 'react';

function DraggableSlider({ min = 0, max = 100, initialValue = 0, onChange }) {
  const [value, setValue] = useState(initialValue);
  const sliderRef = useRef(null);
  const isDragging = useRef(false);

  const handleMouseDown = () => {
    isDragging.current = true;
  };

  const handleMouseUp = () => {
    if (isDragging.current) {
      isDragging.current = false;
    }
    // if (onChange) onChange(value);
  };

  const handleMouseMove = (e) => {
    if (isDragging.current && sliderRef.current) {
      const rect = sliderRef.current.getBoundingClientRect();
      const newValue = Math.min(
        max,
        Math.max(
          min,
          ((e.clientX - rect.left) / rect.width) * (max - min) + min
        )
      );
      setValue(Math.round(newValue));
      // if (onChange && isDragging.current) onChange(newValue);
    }
  };

  useEffect(() => {
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };
  }, []);

  useEffect(() => {
    onChange(value)
  }, [value])

  return (
    <div
      ref={sliderRef}
      className="slider-container relative w-full h-2 bg-gray-300 rounded-md"
      onMouseDown={handleMouseDown}
    >
      <div
        className="slider-thumb absolute top-0 bg-blue-500 rounded-full h-6 w-6 transform -translate-y-2"
        style={{ left: `${((value - min) / (max - min)) * 100}%` }}
      ></div>
    </div>
  );
}

export default DraggableSlider;