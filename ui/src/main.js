import './styles.css';

const app = document.querySelector('#app');

app.innerHTML = `
  <main class="container">
    <header class="header">
      <div>
        <p class="eyebrow">Support automation</p>
        <h1>EPAM DIAL Multi-Model Orchestrator</h1>
      </div>
    </header>

    <section class="card">
      <h2>Ticket classification</h2>
      <textarea id="issue" rows="5">Customer reports duplicate billing and requests a refund for a recent order.</textarea>
      <button id="ticket-btn">Run classification</button>
      <pre id="ticket-output">Waiting for classification...</pre>
    </section>

    <section class="card">
      <h2>Escalation review</h2>
      <textarea id="escalation" rows="5">Ticket T-1542: Customer disputes a policy denial and asks for an exception to the refund rule.</textarea>
      <button id="escalate-btn">Run escalation review</button>
      <pre id="escalation-output">Waiting for escalation review...</pre>
    </section>
  </main>
`;

const apiBase = 'http://localhost:8000';

async function callApi(url, payload) {
  const response = await fetch(`${apiBase}${url}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return response.json();
}

async function runClassification() {
  const issue = document.querySelector('#issue').value;
  const output = document.querySelector('#ticket-output');
  output.textContent = 'Calling the routing API...';

  try {
    const result = await callApi('/api/support/ticket', {
      customer_email: 'customer@example.com',
      issue_summary: issue,
      priority: 'high',
      order_id: 'ORD-9001',
      metadata: { source: 'web-ui' },
    });
    output.textContent = JSON.stringify(result, null, 2);
  } catch (error) {
    output.textContent = `Error: ${error.message}`;
  }
}

async function runEscalation() {
  const issue = document.querySelector('#escalation').value;
  const output = document.querySelector('#escalation-output');
  output.textContent = 'Running policy review...';

  try {
    const result = await callApi('/api/support/escalate', {
      ticket_id: 'T-1542',
      issue_summary: issue,
      customer_profile: 'Returning customer with a long account history',
      policy_context: 'The standard refund policy allows exceptions only for fraud or service outage.',
      previous_attempts: ['Explained the policy', 'Customer asked for a manual review'],
    });
    output.textContent = JSON.stringify(result, null, 2);
  } catch (error) {
    output.textContent = `Error: ${error.message}`;
  }
}

document.querySelector('#ticket-btn').addEventListener('click', runClassification);
document.querySelector('#escalate-btn').addEventListener('click', runEscalation);
