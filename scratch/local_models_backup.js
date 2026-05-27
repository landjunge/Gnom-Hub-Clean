/**
 * Backup of the local model distribution logic for GNOM-Hub.
 * Location in frontend: /frontend/index.html -> assignLocalModels()
 * 
 * Verified working local models list (tested on 2026-05-26):
 * - mistral:latest
 * - gemma2:2b
 * - llama3:latest
 * - qwen2:7b
 * (phi3:latest failed due to timeout)
 */

window.assignLocalModels = async function() {
  const agents = window.llmAgentsListGlobal || [];
  if (!agents.length) return;

  const workingLocalModels = ['mistral:latest', 'gemma2:2b', 'llama3:latest', 'qwen2:7b'];

  const agentPriority = {
    'coderag': 1,       // braucht fettes Modell - komplexe Aufgaben
    'researcherag': 2,  // braucht großes Modell - Analyse
    'writerag': 3,      // gute Textqualität
    'editorag': 4,      // Bearbeitung
    'generalag': 5,     // Allgemein
    'securityag': 6,    // Checks
    'soulag': 7,        // braucht schnelles/flash Modell - Orchestrierung
    'watchdogag': 8     // braucht schnellstes Modell - Monitoring
  };

  function modelScore(m) {
    const ml = m.toLowerCase();
    if (/405b/.test(ml)) return 900;
    if (/120b/.test(ml)) return 800;
    if (/80b/.test(ml)) return 750;
    if (/70b/.test(ml)) return 700;
    if (/31b|30b|26b/.test(ml)) return 600;
    if (/24b/.test(ml)) return 550;
    if (/20b/.test(ml)) return 500;
    if (/12b/.test(ml)) return 400;
    if (/9b/.test(ml)) return 350;
    if (/7b|8b/.test(ml)) return 300;
    if (/3b/.test(ml)) return 200;
    if (/1\.2b|1b/.test(ml)) return 100;
    return 350;
  }

  // Modelle nach Qualität sortieren (beste zuerst)
  const sorted = [...workingLocalModels].sort((a, b) => modelScore(b) - modelScore(a));

  // Agenten nach Priorität sortieren
  const sortedAgents = [...agents].sort((a, b) => {
    const pa = agentPriority[a.name.toLowerCase()] || 99;
    const pb = agentPriority[b.name.toLowerCase()] || 99;
    return pa - pb;
  });

  // Intelligent zuweisen: bestes Modell → wichtigster Agent
  let config = {};
  sortedAgents.forEach((a, i) => {
    const model = sorted[i % sorted.length];
    config[a.name.toLowerCase()] = { provider: 'lokal', model: model };
  });
  await api('POST', '/llm/agents', config);
  await loadLLMConfig();
};
