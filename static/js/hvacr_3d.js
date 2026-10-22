// static/js/hvacr_3d.js

function initHVACR3D(containerId, initialData) {
    const container = document.getElementById(containerId);
    if (!container) return;

    // 1. Scène, Caméra et Rendu
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0b1220);

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.set(12, 8, 15);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);

    // 2. Éclairage Industriel
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 1.2);
    dirLight.position.set(20, 30, 20);
    dirLight.castShadow = true;
    scene.add(dirLight);

    const bluePointLight = new THREE.PointLight(0x38bdf8, 2, 50);
    bluePointLight.position.set(-5, 5, 5);
    scene.add(bluePointLight);

    const redPointLight = new THREE.PointLight(0xf43f5e, 2, 50);
    redPointLight.position.set(5, 5, 5);
    scene.add(redPointLight);

    // Grille de référence technique discrète
    const grid = new THREE.GridHelper(30, 30, 0x26364D, 0x162338);
    grid.position.y = -1.5;
    scene.add(grid);

    // 3. Modélisation Procédurale des Équipements Industriels
    const group = new THREE.Group();

    // Châssis de base
    const baseGeo = new THREE.BoxGeometry(14, 0.4, 10);
    const baseMat = new THREE.MeshStandardMaterial({ color: 0x111c2e, roughness: 0.8 });
    const base = new THREE.Mesh(baseGeo, baseMat);
    base.position.y = -1.3;
    group.add(base);

    // Compresseur Semi-Hermétique (Bleu Industriel)
    const compGeo = new THREE.CylinderGeometry(1.5, 1.5, 2.5, 32);
    const compMat = new THREE.MeshStandardMaterial({ color: 0x2563eb, metalness: 0.5, roughness: 0.3 });
    const compressor = new THREE.Mesh(compGeo, compMat);
    compressor.position.set(-3, 0, 0);
    compressor.castShadow = true;
    compressor.userData = { name: "Compresseur Semi-Hermétique", type: "Compresseur", status: "Actif" };
    group.add(compressor);

    // Moteur du compresseur (Boîte supérieure)
    const motorGeo = new THREE.BoxGeometry(1.8, 1.2, 1.8);
    const motorMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.7 });
    const motor = new THREE.Mesh(motorGeo, motorMat);
    motor.position.set(-3, 1.8, 0);
    group.add(motor);

    // Condenseur à Air (Batterie à ailettes + Ventilateurs)
    const condGeo = new THREE.BoxGeometry(2, 4, 6);
    const condMat = new THREE.MeshStandardMaterial({ color: 0x334155, wireframe: false, roughness: 0.6 });
    const condenser = new THREE.Mesh(condGeo, condMat);
    condenser.position.set(4, 1, 0);
    condenser.userData = { name: "Condenseur à Air", type: "Échangeur HP", status: "Optimal" };
    group.add(condenser);

    // Ventilateurs du Condenseur
    const fanBladeGeo = new THREE.BoxGeometry(2.2, 0.1, 0.4);
    const fanMat = new THREE.MeshStandardMaterial({ color: 0x0f172a });
    const fan1 = new THREE.Mesh(fanBladeGeo, fanMat);
    fan1.position.set(5.1, 1.5, 1.5);
    group.add(fan1);

    const fan2 = new THREE.Mesh(fanBladeGeo, fanMat);
    fan2.position.set(5.1, 1.5, -1.5);
    group.add(fan2);

    // Réservoir / Bouteille liquide
    const tankGeo = new THREE.CylinderGeometry(0.8, 0.8, 3, 16);
    const tankMat = new THREE.MeshStandardMaterial({ color: 0x64748b, metalness: 0.8 });
    const tank = new THREE.Mesh(tankGeo, tankMat);
    tank.position.set(1.5, -0.2, 2.5);
    group.add(tank);

    scene.add(group);

    // 4. Tuyauteries du Cycle Frigorifique (HP en Rouge, BP en Bleu)
    const hpMaterial = new THREE.MeshBasicMaterial({ color: 0xf43f5e }); // Haute Pression
    const bpMaterial = new THREE.MeshBasicMaterial({ color: 0x38bdf8 }); // Basse Pression

    // Tuyau de refoulement (Compresseur -> Condenseur) : HP
    const curveHP = new THREE.QuadraticBezierCurve3(
        new THREE.Vector3(-3, 1.2, 0),
        new THREE.Vector3(0.5, 3.5, 0),
        new THREE.Vector3(4, 2.5, 2)
    );
    const tubeHPGeo = new THREE.TubeGeometry(curveHP, 64, 0.12, 8, false);
    const tubeHP = new THREE.Mesh(tubeHPGeo, hpMaterial);
    scene.add(tubeHP);

    // Tuyau d'aspiration (Condenseur/Réservoir -> Compresseur) : BP
    const curveBP = new THREE.QuadraticBezierCurve3(
        new THREE.Vector3(3, -0.5, 2.5),
        new THREE.Vector3(-0.5, -0.5, -2),
        new THREE.Vector3(-3, -0.5, -1)
    );
    const tubeBPGeo = new THREE.TubeGeometry(curveBP, 64, 0.12, 8, false);
    const tubeBP = new THREE.Mesh(tubeBPGeo, bpMaterial);
    scene.add(tubeBP);

    // 5. Particules animées représentant le flux de fluide frigorigène
    const particleCount = 40;
    const particleGeo = new THREE.SphereGeometry(0.08, 8, 8);
    const particleMat = new THREE.MeshBasicMaterial({ color: 0x22d3ee });
    const particles = [];

    for (let i = 0; i < particleCount; i++) {
        const p = new THREE.Mesh(particleGeo, particleMat);
        scene.add(p);
        particles.push({ mesh: p, progress: i / particleCount });
    }

    // 6. Interaction Souris (Clic pour inspecter un composant)
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    window.addEventListener('click', (event) => {
        const rect = renderer.domElement.getBoundingClientRect();
        if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) return;

        mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(group.children);

        if (intersects.length > 0) {
            const hit = intersects[0].object;
            if (hit.userData && hit.userData.name) {
                const infoBox = document.getElementById('hvacr-info-panel');
                if (infoBox) {
                    infoBox.innerHTML = `<b>Composant :</b> ${hit.userData.name}<br><b>Type :</b> ${hit.userData.type}<br><b>État :</b> <span style="color:#34d399">${hit.userData.status}</span>`;
                }
            }
        }
    });

    // 7. Boucle d'Animation Continue
    let clock = new THREE.Clock();

    function animate() {
        requestAnimationFrame(animate);
        const delta = clock.getDelta();

        // Rotation des ventilateurs du condenseur
        fan1.rotation.x += 5 * delta;
        fan2.rotation.x += 5 * delta;

        // Animation des particules le long de la courbe HP
        particles.forEach((p) => {
            p.progress += 0.3 * delta;
            if (p.progress > 1) p.progress = 0;
            const pos = curveHP.getPointAt(p.progress);
            p.mesh.position.copy(pos);
        });

        // Rotation légère de la caméra pour l'effet vivant (ou contrôles manuels)
        const time = Date.now() * 0.0005;
        camera.position.x = Math.cos(time * 0.5) * 15;
        camera.position.z = Math.sin(time * 0.5) * 15;
        camera.lookAt(0, 0, 0);

        renderer.render(scene, camera);
    }

    animate();

    // Gestion du redimensionnement de la fenêtre
    window.addEventListener('resize', () => {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    });
}