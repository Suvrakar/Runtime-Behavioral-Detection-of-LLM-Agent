const pptxgen = require("pptxgenjs");
const React = require("react");
const RDS = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");

const NAVY="0B2545", BLUE="00629B", LBLUE="E6F0F7", ORANGE="F28C28", RED="C0392B", GREEN="2E8B57", GRAY="5A6572", LG="F3F5F7", WHITE="FFFFFF";
const HF="Cambria", BF="Calibri";

async function icon(Comp, color, size=256){
  const svg = RDS.renderToStaticMarkup(React.createElement(Comp,{color:"#"+color,size:String(size)}));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64,"+buf.toString("base64");
}

(async()=>{
const pres = new pptxgen();
pres.layout="LAYOUT_16x9";
pres.title="Runtime Behavioral Detection of LLM Agent Hijacking from Execution Trajectories";
pres.author="Suvra, Modina, Anika, Abid";

pres.defineSlideMaster({title:"CONTENT",background:{color:WHITE},
  objects:[
   {rect:{x:0,y:5.25,w:10,h:0.375,fill:{color:LBLUE}}},
   {text:{text:"IEEE ICCIT 2026  |  Paper ID 2668  |  TRACE",options:{x:0.5,y:5.27,w:6,h:0.33,fontFace:BF,fontSize:10,color:GRAY,margin:0}}},
  ],
  slideNumber:{x:9.0,y:5.27,w:0.5,h:0.33,fontFace:BF,fontSize:10,color:GRAY,align:"right"}});
pres.defineSlideMaster({title:"DARK",background:{color:NAVY}});

let n=0;
function content(title, notes){
  const s=pres.addSlide({masterName:"CONTENT"});
  s.addText(title,{x:0.5,y:0.3,w:9,h:0.75,fontFace:HF,fontSize:28,bold:true,color:NAVY,margin:0,isTextBox:true,valign:"middle"});
  if(notes) s.addNotes(notes);
  return s;
}
function card(s,x,y,w,h,fill=LG){
  s.addShape(pres.shapes.RECTANGLE,{x,y,w,h,fill:{color:fill},line:{color:"DDE3E8",width:0.75}});
}
function iconCircle(s,data,x,y,d=0.6,fill=BLUE){
  s.addShape(pres.shapes.OVAL,{x,y,w:d,h:d,fill:{color:fill},line:{color:fill}});
  const p=d*0.25; s.addImage({data,x:x+p,y:y+p,w:d-2*p,h:d-2*p});
}
function stat(s,x,y,w,big,label,color=BLUE){
  card(s,x,y,w,1.3);
  s.addText(big,{x,y:y+0.1,w,h:0.7,fontFace:HF,fontSize:34,bold:true,color,align:"center",margin:0,isTextBox:true});
  s.addText(label,{x:x+0.1,y:y+0.78,w:w-0.2,h:0.45,fontFace:BF,fontSize:12,color:GRAY,align:"center",margin:0,isTextBox:true,valign:"top"});
}
const bullets=(arr,sz=16)=>arr.map((t,i)=>({text:t,options:{bullet:true,breakLine:i<arr.length-1,paraSpaceAfter:8,fontSize:sz,fontFace:BF,color:"222222"}}));

// 1. Title
{
 const s=pres.addSlide({masterName:"DARK"});
 s.addText("29th International Conference on Computer and Information Technology (IEEE ICCIT 2026)",{x:0.6,y:0.4,w:8.8,h:0.4,fontFace:BF,fontSize:13,color:"9FC5E0",margin:0,isTextBox:true});
 s.addText("Runtime Behavioral Detection of LLM Agent Hijacking from Execution Trajectories",{x:0.6,y:1.0,w:8.8,h:1.8,fontFace:HF,fontSize:34,bold:true,color:WHITE,margin:0,isTextBox:true,valign:"top"});
 s.addText("Debashis Kar Suvra¹, Jannatul Ferdous Modina², Azrin Nahar Anika², MD Bakhtiar Abid³",{x:0.6,y:3.05,w:8.8,h:0.4,fontFace:BF,fontSize:16,bold:true,color:WHITE,margin:0,isTextBox:true});
 s.addText("¹ Institute of Appropriate Technology, BUET   ² BUBT   ³ BRAC University",{x:0.6,y:3.5,w:8.8,h:0.35,fontFace:BF,fontSize:13,color:"C9DCEA",margin:0,isTextBox:true});
 s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:0.6,y:4.4,w:3.0,h:0.45,fill:{color:ORANGE},line:{color:ORANGE},rectRadius:0.08});
 s.addText("Paper ID 2668  ·  Oral Presentation",{x:0.6,y:4.4,w:3.0,h:0.45,fontFace:BF,fontSize:13,bold:true,color:NAVY,align:"center",valign:"middle",margin:0,isTextBox:true});
 s.addNotes("Introduce yourselves. One-sentence pitch: attackers can hide the trigger text, but not what the agent does afterwards, so we detect hijacking from the execution trajectory.");
}

// 2. Motivation
{
 const s=content("LLM agents are a new attack surface","Agents now read files, call APIs and browse with little oversight. Two attack families dominate: indirect prompt injection and skill/tool poisoning.");
 const ic1=await icon(fa.FaRobot,WHITE), ic2=await icon(fa.FaBug,WHITE), ic3=await icon(fa.FaPlug,WHITE);
 s.addText("Agents orchestrate multi-step workflows—files, APIs, web, code—with little human oversight.",{x:0.5,y:1.15,w:9,h:0.6,fontFace:BF,fontSize:16,color:"222222",margin:0,isTextBox:true});
 const items=[[ic2,"Indirect prompt injection","Malicious instructions hidden in content the agent reads (web pages, files, tool outputs) redirect its next actions."],
              [ic3,"Skill / tool poisoning","A malicious plugin or MCP server behaves harmfully only when the agent invokes it."]];
 items.forEach((it,i)=>{
   const x=0.5+i*4.6; card(s,x,1.95,4.4,2.6);
   iconCircle(s,it[0],x+0.25,2.15,0.7,i?ORANGE:BLUE);
   s.addText(it[1],{x:x+1.1,y:2.15,w:3.2,h:0.7,fontFace:HF,fontSize:18,bold:true,color:NAVY,margin:0,valign:"middle",isTextBox:true});
   s.addText(it[2],{x:x+0.25,y:3.05,w:3.9,h:1.4,fontFace:BF,fontSize:15,color:"222222",margin:0,valign:"top",isTextBox:true});
 });
}

// 3. Problem
{
 const s=content("Text-level defenses inspect only the trigger","Static scanners, guard models and LLM judges look at text before execution. Evasive attacks are engineered so that text looks clean, so these defenses have no signal.");
 const cells=[["Overt injection","Payload visible in retrieved content",LBLUE,NAVY],["Evasive injection","Position-aware, split or paraphrased payload",ORANGE,NAVY],
              ["Overt poisoning","Malicious skill description",LBLUE,NAVY],["Evasive poisoning","Payload-less skill; harm at invocation",ORANGE,NAVY]];
 cells.forEach((c,i)=>{const x=0.5+(i%2)*2.75,y=1.25+Math.floor(i/2)*1.75;
   s.addShape(pres.shapes.RECTANGLE,{x,y,w:2.6,h:1.6,fill:{color:c[2]==ORANGE?"FDEBD3":LBLUE},line:{color:c[2]==ORANGE?ORANGE:BLUE,width:1}});
   s.addText([{text:c[0],options:{bold:true,fontSize:15,breakLine:true,color:NAVY,fontFace:HF}},{text:c[1],options:{fontSize:13,color:"333333",fontFace:BF}}],{x:x+0.12,y:y+0.12,w:2.36,h:1.36,margin:0,valign:"top",isTextBox:true});
 });
 s.addText("Four attack cells",{x:0.5,y:4.8,w:5.3,h:0.3,fontFace:BF,fontSize:12,italic:true,color:GRAY,margin:0,isTextBox:true});
 s.addText(bullets(["Scanners keyword-match text → evasive variants slip through","Keyword scanner detects only 23.6% in our benchmark","Evasive text is clean by design: no textual signal left"],15),{x:6.2,y:1.4,w:3.3,h:3.2,margin:0,valign:"top",isTextBox:true});
}

// 4. Insight + threat model
{
 const s=content("Key insight: triggers hide, behavior does not","A hijacked agent must still perform unauthorized actions, and those appear in the execution log even when the triggering text is clean. TRACE decouples the detection signal (post-execution behavior) from the evasion target (pre-execution text). Threat model: black-box with respect to TRACE; cannot modify framework, detector, or task.");
 card(s,0.5,1.2,4.4,3.7,NAVY);
 s.addText("Hijacking leaves a trace",{x:0.7,y:1.35,w:4.0,h:0.45,fontFace:HF,fontSize:20,bold:true,color:WHITE,margin:0,isTextBox:true});
 s.addText(bullets(["Exfiltrate data to attacker hosts","Contact hosts the task never implied","Invoke unauthorized or privileged tools"],15).map(b=>{b.options.color=WHITE;return b;}),{x:0.7,y:1.95,w:4.0,h:1.9,margin:0,valign:"top",isTextBox:true});
 s.addText("All visible as tool calls, arguments and destinations in the log.",{x:0.7,y:4.0,w:4.0,h:0.7,fontFace:BF,fontSize:14,italic:true,color:"CFE3F1",margin:0,isTextBox:true,valign:"top"});
 card(s,5.1,1.2,4.4,3.7);
 s.addText("Threat model",{x:5.3,y:1.35,w:4.0,h:0.45,fontFace:HF,fontSize:20,bold:true,color:NAVY,margin:0,isTextBox:true});
 s.addText(bullets(["Attacker controls content the agent reads, or publishes a poisoned skill","Cannot change the agent, TRACE, or the task","Black-box w.r.t. TRACE weights and threshold θ","Defender sees only structured execution logs"],14),{x:5.3,y:1.9,w:4.0,h:2.9,margin:0,valign:"top",isTextBox:true});
}

// 5. Architecture
{
 const s=content("TRACE: a passive, CPU-only trajectory detector","The telemetry layer is passive and non-intercepting. Features are extracted from the log and task, scored by a LightGBM classifier. One threshold theta controls the security-utility tradeoff.");
 const steps=[["LLM Agent","any framework"],["Telemetry","passive log ℓ"],["Features","φ(ℓ,τ), 30-dim"],["Classifier","LightGBM score s"]];
 steps.forEach((t,i)=>{const x=0.5+i*2.35;
   s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y:1.5,w:1.95,h:1.1,fill:{color:i==3?BLUE:LBLUE},line:{color:BLUE,width:1},rectRadius:0.1});
   s.addText([{text:t[0],options:{bold:true,fontSize:15,breakLine:true,fontFace:HF}},{text:t[1],options:{fontSize:12,fontFace:BF}}],{x,y:1.5,w:1.95,h:1.1,align:"center",valign:"middle",color:i==3?WHITE:NAVY,margin:0,isTextBox:true});
   if(i<3) s.addText("→",{x:x+1.95,y:1.75,w:0.4,h:0.6,fontSize:24,bold:true,color:ORANGE,align:"center",margin:0,isTextBox:true});
 });
 s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:3.3,y:3.2,w:1.7,h:0.6,fill:{color:"DFF2E6"},line:{color:GREEN},rectRadius:0.08});
 s.addText("ALLOW  s ≤ θ",{x:3.3,y:3.2,w:1.7,h:0.6,align:"center",valign:"middle",fontSize:14,bold:true,color:GREEN,margin:0,isTextBox:true});
 s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:5.2,y:3.2,w:1.7,h:0.6,fill:{color:"F8DEDA"},line:{color:RED},rectRadius:0.08});
 s.addText("BLOCK  s > θ",{x:5.2,y:3.2,w:1.7,h:0.6,align:"center",valign:"middle",fontSize:14,bold:true,color:RED,margin:0,isTextBox:true});
 s.addText("Two modes: run-level (whole trajectory) and step-level (every prefix)",{x:0.5,y:4.2,w:9,h:0.4,fontFace:BF,fontSize:15,color:"222222",margin:0,isTextBox:true});
 s.addText("No model weights, logits or prompts needed · no agent modification · 0.67 ms per query on a laptop CPU",{x:0.5,y:4.65,w:9,h:0.4,fontFace:BF,fontSize:14,italic:true,color:GRAY,margin:0,isTextBox:true});
}

// 6. Features
{
 const s=content("Thirty behavioral features in five groups","F1 sequence bigrams and unigrams; F2 base64, external hosts, deep paths, long args, POSTs; F3 fraction of network calls outside the task-implied allow-list; F4 TF-IDF cosine distance between task and actions; F5 structural counts. F1 and F3 carry most of the signal.");
 const rows=[["F1","Sequence n-grams","Tool-name bigrams/unigrams (15 dims)"],["F2","Argument anomalies","base64, external hosts, deep paths, long args, POSTs"],["F3","Network destination","Share of calls to hosts outside task-implied list"],["F4","Intent–action","TF-IDF cosine distance: task vs. actions"],["F5","Structure","Steps, tool diversity, loops, privileged tools, failures"]];
 rows.forEach((r,i)=>{const y=1.2+i*0.76;
   card(s,0.5,y,9,0.66);
   s.addShape(pres.shapes.OVAL,{x:0.65,y:y+0.09,w:0.48,h:0.48,fill:{color:i==0||i==2?ORANGE:BLUE},line:{color:WHITE}});
   s.addText(r[0],{x:0.65,y:y+0.09,w:0.48,h:0.48,fontSize:13,bold:true,color:WHITE,align:"center",valign:"middle",margin:0,isTextBox:true});
   s.addText(r[1],{x:1.35,y,w:2.5,h:0.66,fontFace:HF,fontSize:16,bold:true,color:NAVY,valign:"middle",margin:0,isTextBox:true});
   s.addText(r[2],{x:3.9,y,w:5.5,h:0.66,fontFace:BF,fontSize:14,color:"222222",valign:"middle",margin:0,isTextBox:true});
 });
}

// 7. Setup
{
 const s=content("Benchmark: 1,133 trajectories, five LLMs","All tools are simulated stubs. Corpus of 539 attack and 594 benign trajectories from five generator models via OpenRouter; 60/20/20 split stratified by attack cell and model; test split has 228 trajectories. Leave-one-template-out CV guards against template memorization.");
 stat(s,0.5,1.2,2.1,"1,133","trajectories");
 stat(s,2.75,1.2,2.1,"539","attack");
 stat(s,5.0,1.2,2.1,"594","benign");
 stat(s,7.25,1.2,2.25,"5","generator LLMs",ORANGE);
 s.addText(bullets(["Four attack cells: overt/evasive × injection/poisoning","Models: Gemini 2.5 Flash Lite, Llama 3.1 8B / 3.2 3B, Mistral Nemo, Qwen 2.5 7B","60/20/20 split, stratified; test set = 110 attack + 118 benign","Leave-one-template-out CV: AUC 0.983, DR 92.3%, FPR 5.5%","Baselines: keyword scanner, behavioral rules, LR, Random Forest"],15),{x:0.5,y:2.8,w:9,h:2.3,margin:0,valign:"top",isTextBox:true});
}

// 8. RQ1 baseline chart
{
 const s=content("RQ1: behavior beats text-level baselines","On the held-out test split at theta 0.5, TRACE reaches AUC 0.986 [0.967-0.998] and 93.6% detection at 2.5% FPR. The keyword scanner reaches 23.6% and behavioral rules 44.5%. TRACE and Random Forest are not statistically distinguishable.");
 s.addChart(pres.charts.BAR,[{name:"Detection rate (%)",labels:["Keyword scanner","Behavioral rules","LR (F1 only)","LR (all)","Random Forest","TRACE"],values:[23.6,44.5,64.5,87.3,92.7,93.6]}],
  {x:0.5,y:1.15,w:5.6,h:4.0,barDir:"bar",chartColors:[BLUE],showValue:true,dataLabelFontSize:12,dataLabelColor:"222222",dataLabelFormatCode:"0.0",
   catAxisLabelFontSize:12,catAxisLabelColor:"333333",valAxisLabelFontSize:11,valAxisLabelColor:GRAY,valAxisMaxVal:100,valAxisMinVal:0,
   valGridLine:{color:"E3E7EA",size:0.5},catGridLine:{style:"none"},showLegend:false,catAxisOrientation:"maxMin",showTitle:true,title:"Detection rate (%) at θ=0.5",titleFontSize:13,titleColor:NAVY});
 stat(s,6.4,1.2,3.1,"0.986","AUC  [0.967–0.998]");
 stat(s,6.4,2.65,3.1,"93.6%","detection at 2.5% FPR",ORANGE);
 s.addText("TRACE ≈ Random Forest (CIs overlap); both far above rules and scanner.",{x:6.4,y:4.1,w:3.1,h:0.9,fontFace:BF,fontSize:12,italic:true,color:GRAY,margin:0,isTextBox:true,valign:"top"});
}

// 9. RQ2 evasion
{
 const s=content("RQ2: evasive attacks still leave behavioral traces","TRACE detects 90.0 to 96.2 percent across all four attack cells, with injection-evasive the lowest and poisoning-overt the highest. The keyword scanner detects only 23.6 percent in aggregate because evasive text is clean.");
 stat(s,0.5,1.3,2.9,"90.0%","lowest cell: evasive injection",ORANGE);
 stat(s,3.55,1.3,2.9,"96.2%","highest cell: overt poisoning",GREEN);
 stat(s,6.6,1.3,2.9,"23.6%","keyword scanner (aggregate)",RED);
 s.addText(bullets(["TRACE stays at 90–96% DR in every attack cell (n = 25–30 per cell)","Text-level inspection fails on evasive variants by construction","Behavior, not phrasing, carries the signal"],16),{x:0.5,y:3.0,w:9,h:1.9,margin:0,valign:"top",isTextBox:true});
}

// 10. Frontier
{
 const s=content("Security–utility frontier, tuned by θ","Sweeping theta traces the Pareto frontier. At theta 0.27, TRACE gets 96.4 percent security at 95.8 percent utility. Lowering theta to 0.01 reaches 97.3 percent security at 88.1 percent utility. A scanner offers one fixed point.");
 s.addChart(pres.charts.SCATTER,[{name:"X",values:[50,88.1,95.8,100]},{name:"TRACE (behavioral)",values:[100,97.3,96.4,0]}],
  {x:0.5,y:1.15,w:5.8,h:4.0,chartColors:[BLUE],lineSize:2,lineDataSymbolSize:9,showLegend:false,valAxisMinVal:0,valAxisMaxVal:100,catAxisMinVal:50,catAxisMaxVal:100,
   showCatAxisTitle:true,catAxisTitle:"Legitimate utility preserved (%)",showValAxisTitle:true,valAxisTitle:"Attack detection rate (%)",catAxisTitleFontSize:11,valAxisTitleFontSize:11,
   catAxisLabelFontSize:11,valAxisLabelFontSize:11,catAxisLabelColor:GRAY,valAxisLabelColor:GRAY,valGridLine:{color:"E3E7EA",size:0.5},catGridLine:{color:"E3E7EA",size:0.5}});
 stat(s,6.6,1.2,2.9,"96.4%","security at θ=0.27",BLUE);
 stat(s,6.6,2.65,2.9,"95.8%","utility at θ=0.27",GREEN);
 s.addText("Keyword scanner: a single fixed point at 23.6% detection, no tunable trade-off.",{x:6.6,y:4.1,w:2.9,h:0.9,fontFace:BF,fontSize:12,italic:true,color:GRAY,margin:0,isTextBox:true,valign:"top"});
}

// 11. Ablation
{
 const s=content("Ablation: F1 and F3 carry most of the power","Dropping F1 costs 0.025 AUC; F3 alone reaches 0.738; F1 plus F3 reaches 0.972. On a small test split near the AUC ceiling, deltas near zero may reflect measurement resolution rather than strict redundancy.");
 s.addChart(pres.charts.BAR,[{name:"AUC",labels:["Full TRACE","− F1","− F2","− F3","− F4","− F5","F3 alone","F1 + F3"],values:[0.986,0.961,0.983,0.985,0.974,0.983,0.738,0.972]}],
  {x:0.5,y:1.15,w:6.2,h:4.0,barDir:"col",chartColors:[BLUE],showValue:true,dataLabelFontSize:11,dataLabelColor:"222222",dataLabelFormatCode:"0.000",
   catAxisLabelFontSize:11,catAxisLabelColor:"333333",valAxisLabelFontSize:11,valAxisLabelColor:GRAY,valAxisMinVal:0.6,valAxisMaxVal:1.0,
   valGridLine:{color:"E3E7EA",size:0.5},catGridLine:{style:"none"},showLegend:false,showTitle:true,title:"Test AUC by feature configuration",titleFontSize:13,titleColor:NAVY});
 s.addText(bullets(["No single group dominates","Removing F1: −0.025 AUC (largest drop)","F1+F3 alone recovers 0.972","Deltas near the ceiling are within noise"],14),{x:6.95,y:1.4,w:2.6,h:3.4,margin:0,valign:"top",isTextBox:true});
}

// 12. Cross-model
{
 const s=content("RQ3: cross-model transfer is the weak spot","Rows are training model, columns are test model. In-distribution AUC is 0.93 to 1.00. Within the Llama family transfer is strong; across families it drops sharply, as low as 0.61. Hypothesis H2, that transfer drops by less than 0.05 AUC, is not confirmed. Per-deployment calibration on benign logs is required.");
 const M=[["M1",1.000,0.799,0.908,0.636,0.611],["M2",0.917,0.932,0.931,0.854,0.851],["M3",1.000,0.904,0.983,0.705,0.618],["M4",0.858,0.883,0.849,0.935,0.906],["M5",0.767,0.873,0.828,0.903,0.991]];
 const hdr=["Train → Test","M1","M2","M3","M4","M5"].map(t=>({text:t,options:{bold:true,color:WHITE,fill:{color:NAVY},align:"center",fontSize:13,fontFace:BF}}));
 const rows=[hdr];
 M.forEach((r,i)=>rows.push(r.map((v,j)=>{
   if(j==0) return {text:v,options:{bold:true,align:"center",fill:{color:LBLUE},color:NAVY,fontSize:13,fontFace:BF}};
   const diag=i+1==j; const f=diag?"CFE3F1":(v>=0.9?"DFF2E6":(v>=0.8?"FFF4D6":"F8DEDA"));
   return {text:v.toFixed(3),options:{align:"center",fill:{color:f},color:"222222",bold:diag,fontSize:13,fontFace:BF}};})));
 s.addTable(rows,{x:0.5,y:1.2,w:5.6,colW:[1.35,0.85,0.85,0.85,0.85,0.85],rowH:0.5,border:{type:"solid",pt:0.75,color:"FFFFFF"}});
 s.addText("Blue = in-distribution · green ≥ 0.90 · yellow 0.80–0.90 · red < 0.80",{x:0.5,y:4.35,w:5.6,h:0.5,fontFace:BF,fontSize:11,italic:true,color:GRAY,margin:0,isTextBox:true});
 s.addText(bullets(["Within Llama family: strong (0.85–0.87)","Cross-family: sharp drop (down to 0.61)","H2 not confirmed","Fix: calibrate θ or refit on target benign logs"],14),{x:6.4,y:1.3,w:3.1,h:3.6,margin:0,valign:"top",isTextBox:true});
}

// 13. Adaptive
{
 const s=content("Adaptive attackers degrade detection","Exp G suppresses features at inference on attack trajectories. F3 suppression alone barely hurts; F1 suppression costs 16 points of detection; full F1+F2+F3 suppression leaves only F4/F5 signal and DR 54.5 percent, still 2.3 times the keyword scanner.");
 s.addChart(pres.charts.BAR,[{name:"DR",labels:["No suppression","F3 suppressed","F1 suppressed","F1+F3","F1+F2+F3"],values:[93.6,90.9,77.3,72.7,54.5]}],
  {x:0.5,y:1.15,w:6.0,h:4.0,barDir:"col",chartColors:[BLUE],showValue:true,dataLabelFontSize:12,dataLabelColor:"222222",dataLabelFormatCode:"0.0",
   catAxisLabelFontSize:11,catAxisLabelColor:"333333",valAxisLabelFontSize:11,valAxisLabelColor:GRAY,valAxisMinVal:0,valAxisMaxVal:100,
   valGridLine:{color:"E3E7EA",size:0.5},catGridLine:{style:"none"},showLegend:false,showTitle:true,title:"Detection rate (%) under feature suppression",titleFontSize:13,titleColor:NAVY});
 stat(s,6.8,1.3,2.7,"54.5%","DR under full F1+F2+F3 suppression",RED);
 stat(s,6.8,2.8,2.7,"2.3×","still above keyword scanner",GREEN);
 s.addText("Full gradient-based attacks remain future work.",{x:6.8,y:4.3,w:2.7,h:0.6,fontFace:BF,fontSize:12,italic:true,color:GRAY,margin:0,isTextBox:true,valign:"top"});
}

// 14. Step-level & latency
{
 const s=content("Step-level mode and latency","Step-level mode at theta 0.08 flags 99.1 percent of attacks before the trajectory ends, median detection step 1. But scoring every prefix flags 80.5 percent of benign trajectories at least once, versus 6.8 percent for run-level, because the classifier is trained on complete trajectories. This is a recall-oriented trigger, not a deployable blocker, until prefix-aware training is done. Latency: 0.64 to 0.67 ms per query single, 0.002 ms per trajectory batched; feature extraction 1.2 ms for a 10-step trajectory. Concurrent multi-agent load and long-horizon trajectories were not measured.");
 stat(s,0.5,1.2,2.1,"99.1%","attacks flagged before the end",GREEN);
 stat(s,2.75,1.2,2.1,"step 1","median detection step",BLUE);
 stat(s,5.0,1.2,2.1,"80.5%","benign prefix FPR at θ=0.08",RED);
 stat(s,7.25,1.2,2.25,"0.67 ms","per query (CPU)",ORANGE);
 card(s,0.5,2.75,9,2.3,"FDF1E3");
 s.addText("Honest caveat",{x:0.7,y:2.85,w:8.6,h:0.4,fontFace:HF,fontSize:18,bold:true,color:NAVY,margin:0,isTextBox:true});
 s.addText(bullets(["Run-level FPR at θ=0.08 is 6.8%, but 80.5% of benign runs trip on some prefix","Remedy (untested): prefix-augmented training and a minimum prefix length","Scoring is stateless per trajectory → scales horizontally; concurrent and long-horizon load not measured"],14),{x:0.7,y:3.3,w:8.6,h:1.7,margin:0,valign:"top",isTextBox:true});
}

// 15. Limitations & future work
{
 const s=content("Limitations and future work","All tools are simulated stubs and the template bank is small (15 attack, 25 benign), so results are in-benchmark estimates. Mimicry defenses listed are proposals, not evaluated results.");
 card(s,0.5,1.2,4.4,3.8);
 s.addText("Limitations",{x:0.7,y:1.3,w:4,h:0.4,fontFace:HF,fontSize:20,bold:true,color:NAVY,margin:0,isTextBox:true});
 s.addText(bullets(["Simulated tools, five-tool environment","Small template bank (15 / 25)","LLM-simulated trajectories may leak simulation artifacts","Cross-model transfer weak","Step-level FPR high"],14),{x:0.7,y:1.8,w:4.0,h:3.1,margin:0,valign:"top",isTextBox:true});
 card(s,5.1,1.2,4.4,3.8,LBLUE);
 s.addText("Future work (not yet evaluated)",{x:5.3,y:1.3,w:4,h:0.4,fontFace:HF,fontSize:20,bold:true,color:NAVY,margin:0,isTextBox:true});
 s.addText(bullets(["Gateway-enforced host allow-list","Taint tracking: untrusted input → network writes","Adversarial training on suppressed attacks","Sequence models over event streams","Validation on live agent traces"],14),{x:5.3,y:1.8,w:4.0,h:3.1,margin:0,valign:"top",isTextBox:true});
}

// 16. Conclusion
{
 const s=pres.addSlide({masterName:"DARK"});
 s.addText("Conclusions",{x:0.6,y:0.4,w:8.8,h:0.7,fontFace:HF,fontSize:34,bold:true,color:WHITE,margin:0,isTextBox:true});
 const pts=[["1","Behavior survives text evasion","AUC 0.986; 90.0–96.2% DR in every attack cell vs. 23.6% for a keyword scanner"],["2","Tunable and lightweight","FPR-calibrated frontier; CPU-only; 0.67 ms per query"],["3","Open challenges","Cross-model calibration, adaptive attackers (54.5% DR), step-level false positives"]];
 pts.forEach((p,i)=>{const y=1.35+i*1.2;
   s.addShape(pres.shapes.OVAL,{x:0.6,y:y+0.1,w:0.7,h:0.7,fill:{color:ORANGE},line:{color:ORANGE}});
   s.addText(p[0],{x:0.6,y:y+0.1,w:0.7,h:0.7,fontFace:HF,fontSize:22,bold:true,color:NAVY,align:"center",valign:"middle",margin:0,isTextBox:true});
   s.addText(p[1],{x:1.6,y,w:7.8,h:0.45,fontFace:HF,fontSize:20,bold:true,color:WHITE,margin:0,isTextBox:true});
   s.addText(p[2],{x:1.6,y:y+0.45,w:7.8,h:0.6,fontFace:BF,fontSize:15,color:"CFE3F1",margin:0,valign:"top",isTextBox:true});
 });
 s.addNotes("Close with: behavioral trajectories are a durable detection signal; we are honest about cross-model transfer and adaptive attackers.");
}

// 17. Thank you
{
 const s=pres.addSlide({masterName:"DARK"});
 const gh=await icon(fa.FaGithub,WHITE);
 s.addText("Thank you — questions?",{x:0.6,y:1.2,w:8.8,h:1.0,fontFace:HF,fontSize:40,bold:true,color:WHITE,margin:0,isTextBox:true});
 s.addImage({data:gh,x:0.6,y:2.6,w:0.5,h:0.5});
 s.addText("github.com/Suvrakar/Runtime-Behavioral-Detection-of-LLM-Agent\nCorpus, features and trained weights released; classifier experiments reproduce without any LLM API calls.",{x:1.3,y:2.5,w:8,h:0.8,fontFace:BF,fontSize:15,color:"CFE3F1",margin:0,isTextBox:true,valign:"middle"});
 s.addText("Debashis Kar Suvra · 0421292001@iat.buet.ac.bd",{x:0.6,y:4.5,w:8.8,h:0.4,fontFace:BF,fontSize:14,color:"9FC5E0",margin:0,isTextBox:true});
 s.addNotes("Likely questions: feature generalization across models (F3/F2 semantic, F1 model-specific); mimicry adversaries (gateway allow-list, taint tracking); scalability (stateless, 0.67 ms; concurrent load not measured).");
}

await pres.writeFile({fileName:"TRACE_ICCIT2026_presentation.pptx"});
console.log("ok");
})().catch(e=>{console.error(e);process.exit(1)});
