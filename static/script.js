// Scene Setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('orbit-container').appendChild(renderer.domElement);

// Earth Sphere
const geometry = new THREE.SphereGeometry(1, 64, 64);
const texture = new THREE.TextureLoader().load("/static/earth_texture.jpg");
const material = new THREE.MeshBasicMaterial({ map: texture });
const earth = new THREE.Mesh(geometry, material);
scene.add(earth);

// Satellite Marker
const satelliteGeometry = new THREE.SphereGeometry(0.05, 32, 32);
const satelliteMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });
const satellite = new THREE.Mesh(satelliteGeometry, satelliteMaterial);
scene.add(satellite);

// Fetch Orbit Data
fetch('/orbit_data')
    .then(response => response.json())
    .then(orbitData => {
        let index = 0;
        
        function animate() {
            requestAnimationFrame(animate);
            
            // Rotate Earth
            earth.rotation.y += 0.001;

            // Update Satellite Position
            if (index < orbitData.length) {
                let [x, y, z] = orbitData[index];
                satellite.position.set(x / 7000, y / 7000, z / 7000); // Scale down
                index = (index + 1) % orbitData.length;
            }

            renderer.render(scene, camera);
        }
        animate();
    });

// Position the camera
camera.position.z = 3;

// Handle Window Resize
window.addEventListener('resize', function() {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
});

