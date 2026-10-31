import React, { useEffect, useRef } from 'react';

export default function CursorFollower() {
  const auraRef = useRef(null);
  const coreRef = useRef(null);

  useEffect(() => {
    // Disable on touch devices
    if (window.matchMedia('(pointer: coarse)').matches) return;

    let mouseX = -100, mouseY = -100;
    let auraX = -100, auraY = -100;
    let animId;

    const onMouseMove = (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      if (coreRef.current) {
        coreRef.current.style.transform = `translate3d(${mouseX}px, ${mouseY}px, 0)`;
      }
    };

    const onMouseDown = () => {
      if (auraRef.current) {
        auraRef.current.style.width = '48px';
        auraRef.current.style.height = '48px';
      }
    };

    const onMouseUp = () => {
      if (auraRef.current) {
        auraRef.current.style.width = '34px';
        auraRef.current.style.height = '34px';
      }
    };

    const animate = () => {
      auraX += (mouseX - auraX) * 0.22;
      auraY += (mouseY - auraY) * 0.22;
      if (auraRef.current) {
        auraRef.current.style.transform = `translate3d(${auraX}px, ${auraY}px, 0)`;
      }
      animId = requestAnimationFrame(animate);
    };

    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mouseup', onMouseUp);
    animId = requestAnimationFrame(animate);

    return () => {
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mousedown', onMouseDown);
      window.removeEventListener('mouseup', onMouseUp);
      cancelAnimationFrame(animId);
    };
  }, []);

  return (
    <>
      <div
        ref={auraRef}
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '34px',
          height: '34px',
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(236, 72, 153, 0.55) 0%, rgba(139, 92, 246, 0.25) 50%, transparent 75%)',
          pointerEvents: 'none',
          zIndex: 999999,
          marginTop: '-17px',
          marginLeft: '-17px',
          mixBlendMode: 'screen',
          filter: 'drop-shadow(0 0 10px rgba(236, 72, 153, 0.7))',
          transition: 'width 0.2s ease, height 0.2s ease'
        }}
      />
      <div
        ref={coreRef}
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '7px',
          height: '7px',
          borderRadius: '50%',
          background: '#ffffff',
          pointerEvents: 'none',
          zIndex: 1000000,
          marginTop: '-3.5px',
          marginLeft: '-3.5px',
          boxShadow: '0 0 8px #c084fc, 0 0 14px #ec4899'
        }}
      />
    </>
  );
}
