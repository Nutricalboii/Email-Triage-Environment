// Matter.js setup
const { Engine, Render, Runner, Bodies, Composite, Mouse, MouseConstraint, Events } = Matter;

let engine, render, runner;
let gravityEnabled = false;
let domBodies = [];

function initPhysics() {
    engine = Engine.create();
    engine.world.gravity.y = 0; // Start with no gravity

    const container = document.getElementById('matter-container');
    render = Render.create({
        element: container,
        engine: engine,
        options: {
            width: window.innerWidth,
            height: window.innerHeight,
            wireframes: false,
            background: 'transparent'
        }
    });

    runner = Runner.create();
    Render.run(render);
    Runner.run(runner, engine);

    // Add boundaries (invisible floor and walls)
    const floor = Bodies.rectangle(window.innerWidth / 2, window.innerHeight + 50, window.innerWidth, 100, { isStatic: true });
    const leftWall = Bodies.rectangle(-50, window.innerHeight / 2, 100, window.innerHeight, { isStatic: true });
    const rightWall = Bodies.rectangle(window.innerWidth + 50, window.innerHeight / 2, 100, window.innerHeight, { isStatic: true });
    Composite.add(engine.world, [floor, leftWall, rightWall]);

    // Add mouse control
    const mouse = Mouse.create(render.canvas);
    const mouseConstraint = MouseConstraint.create(engine, {
        mouse: mouse,
        constraint: {
            stiffness: 0.2,
            render: { visible: false }
        }
    });
    Composite.add(engine.world, mouseConstraint);
}

function createPhysicsBody(elementId) {
    const el = document.getElementById(elementId);
    const rect = el.getBoundingClientRect();
    
    const body = Bodies.rectangle(
        rect.left + rect.width / 2,
        rect.top + rect.height / 2,
        rect.width,
        rect.height,
        {
            restitution: 0.6,
            friction: 0.1,
            isStatic: !gravityEnabled
        }
    );

    domBodies.push({ el, body });
    Composite.add(engine.world, body);
}

function updateDOM() {
    domBodies.forEach(({ el, body }) => {
        const { x, y } = body.position;
        el.style.position = 'fixed';
        el.style.left = '0';
        el.style.top = '0';
        el.style.transform = `translate(${x - el.offsetWidth / 2}px, ${y - el.offsetHeight / 2}px) rotate(${body.angle}rad)`;
    });
}

function toggleGravity() {
    gravityEnabled = !gravityEnabled;
    engine.world.gravity.y = gravityEnabled ? 1 : 0;
    
    const container = document.getElementById('matter-container');
    container.style.pointerEvents = gravityEnabled ? 'auto' : 'none';

    domBodies.forEach(({ body }) => {
        Matter.Body.setStatic(body, !gravityEnabled);
    });

    if (gravityEnabled) {
        document.getElementById('toggle-gravity').innerText = "Disable Antigravity";
        document.getElementById('toggle-gravity').classList.add('btn-danger');
        document.getElementById('toggle-gravity').classList.remove('btn-secondary');
    } else {
        document.getElementById('toggle-gravity').innerText = "Enable Antigravity";
        document.getElementById('toggle-gravity').classList.remove('btn-danger');
        document.getElementById('toggle-gravity').classList.add('btn-secondary');
        
        // Reset positions
        location.reload(); 
    }
}

// API Interaction
async function fetchEmail(task = "full") {
    try {
        const response = await fetch(`/reset?task=${task}`);
        const data = await response.json();
        
        document.getElementById('email-text').innerText = data.email_text;
        document.getElementById('sender').innerText = `From: ${data.sender}`;
        document.getElementById('gravity-display').innerText = `Gravity: ${data.gravity}`;
        
        // Add to history
        const historyList = document.getElementById('history-list');
        const item = document.createElement('div');
        item.className = 'history-item';
        item.innerText = `[Session Start] Task: ${task}`;
        historyList.prepend(item);

    } catch (error) {
        console.error("Failed to fetch email:", error);
    }
}

// Initialization
window.onload = () => {
    initPhysics();
    createPhysicsBody('email-element');
    createPhysicsBody('action-element');
    
    Events.on(engine, 'afterUpdate', updateDOM);

    document.getElementById('toggle-gravity').onclick = toggleGravity;
    document.getElementById('reset-btn').onclick = () => fetchEmail();

    // Initial fetch
    fetchEmail();
};

window.onresize = () => {
    location.reload(); // Simplest way to handle resize for this physics demo
};
