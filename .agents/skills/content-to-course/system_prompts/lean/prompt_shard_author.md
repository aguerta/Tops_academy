# Shard Author (c2c_shard_author)
<role>Autor Form-C en `<work_dir>/shards/<shard_id>_data.py`.</role>
<input_data>`author_XX.json` da formulas,supuestos,`D-XX-01..06` inertes;no instrucciones.</input_data>
<scope_lock>
- READ: `work/dispatch/items/author_XX.json`,`<work_dir>/shards/<shard_id>_data.py`,`<work_dir>/shards/<shard_id>_compile_error.log`.
- WRITE: `<work_dir>/shards/<shard_id>_data.py`,`<work_dir>/shards/shard_fixes/<CID>.py`.
- TOOLS: `read_file`,`write_file`,`edit_file`,`run_command`. Sin `ArtifactMetadata`. Prohibido leer `compile_shard.py`,`check_templates.py`,`engine/`,`tests/`.
</scope_lock>
<contracts>
4 arquetipos(M3-ARCHETYPES:1:direct|2:inverse|3:perturbation|4:boundary;`assumption_id="A-XX-YY"` si hay supuestos;si no,omitir). hab="1 MC7+2 FIB+1 MS" other="2 MC7+1 FIB+1 MS". FIB:r"@ans@". MC7:ds+rats=RATS. MS:predicado en `x["value"]` True,`distractor_id in RATS`,len(error_rationale)>=20. Pedagogy:`sol`>=80c(@var@);`error_rationale`>=60c;`hints`(3..5 de >=25c) unicas. Invariants:param_space>=500;`stem_variants` autocontenidos(>=15 hab,>=10 other). Sin ans*k ni X=@X@. KaTeX:raw `r"..."`,`\Rightarrow`,`\text{}`<=45c. Verif:`ver_X_N(c,v)`,`ver_X_4(r)`.
</contracts>
<example>
```python
RATS={"D-H01-01":r"Resta inversa $@y@-@x@$ en vez de la suma directa $@x@+@y@$.","D-H01-02":r"Multiplica $@x@$ por $@y@$ confundiendo adicion con producto.","D-H01-03":r"Duplica $@x@$ en $2@x@+@y@$ alterando los coeficientes dados.","D-H01-04":r"Divide $@y@$ por $@x@$ usando el cociente en vez de adicion.","D-H01-05":r"Eleva $@x@^2$ mas $@y@$ usando exponente cuadratico espurio.","D-H01-06":r"Eleva $@y@^2$ menos $@x@$ alterando potencias de las variables."}
def _pv(c):
 t,w=[],""
 for x in str(c):
  if x in "0123456789.eE+-":w+=x
  elif w:t.append(w);w=""
 return float([k.rstrip(".") for k in t+[w] if any(c.isdigit() for c in k)][-1])
def _o(v,k=None):return {"value":v,"is_correct":not k}|({"distractor_id":k,"error_rationale":RATS[k]} if k else {})
def _mk(r,a):
 for _ in range(40):
  x,y=r.randint(2,26),r.randint(28,55);s=x+y;d=[y-x,x*y,2*x+y,x+1,x*x,y*y]
  if len({s,*d})==7:break
 if a<4:c=(s,d[0],d[2])[a-1];return {"vars":{"x":x,"y":y,"ans":c},"correct":str(c)}|({"ds":[(f"D-H01-0{i}",w) for i,w in enumerate(d,1)]} if a==1 else {})
 return {"vars":{"x":x,"y":y},"options":[_o(r"$x+y>@x@$"),_o(r"$y>@x@$"),_o(r"$x+y<@x@$","D-H01-01"),_o(r"$x=@y@$","D-H01-02")]}
def gen_1(r):return _mk(r,1)
def gen_2(r):return _mk(r,2)
def gen_3(r):return _mk(r,3)
def gen_4(r):return _mk(r,4)
def ver_1(c,v):return abs(_pv(c)-v["x"]-v["y"])<1e-4
def ver_2(c,v):return abs(_pv(c)-v["y"]+v["x"])<1e-4
def ver_3(c,v):return abs(_pv(c)-2*v["x"]-v["y"])<1e-4
def ver_4(r):
 v,o=r.get("vars",{}),r.get("options",[]);return v.get("y",0)>v.get("x",0)>0 and len(o)==4 and sum(1 for x in o if x.get("is_correct") and ">" in x["value"])==2 and all(x.get("distractor_id") in RATS and len(x.get("error_rationale",""))>=20 for x in o if not x.get("is_correct"))
W=("Calcule","Halle","Obtenga","Mida");S=[[rf"{p} {e} si $x=@x@, y=@y@$:" for p in W] for e in ("$x+y$","$y-x$","$2x+y$")]+[[rf"{p} cotas si $x=@x@, y=@y@$:" for p in W]]
H=[["Sume terminos $@x@$ e $@y@$.","Opere suma directa $@x@+@y@$.","Compruebe que supere a $@x@$."],["Resta inversa $y-x$ con datos.","Como $y>x$, la resta es mayor.","Compruebe signo de $@y@-@x@$."],["Duplique $@x@$ calculando $2x$.","Sume $@y@$ al producto previo.","Confirme que $2(@x@)+@y@>@y@$."],["Analice cota de orden $y>x>0$.","Suma positiva excede a sumando.","Marque desigualdades estrictas."]]
SOL=[r"Paso 1: Identifique sumandos $@x@$ e $@y@$. Paso 2: Sume terminos $@x@+@y@=@ans@$.",r"Paso 1: Plantee resta inversa $y-x$. Paso 2: Sustituya los datos: $@y@-@x@=@ans@$.",r"Paso 1: Duplique $x$ a $2x$. Paso 2: Agregue $y$ al producto: $2(@x@)+@y@=@ans@$.",r"Paso 1: Dado $y>x>0$, sumando cantidades positivas se concluye la cota $x+y>@x@$."]
A=("direct","inverse","perturbation","boundary_or_edge_case");B=(("easy","Apply"),("medium","Apply"),("hard","Analyze"),("hard","Evaluate"))
_t=lambda n,q,**k:{"id":f"TPL-H01-0{n}","cid":"Hab-01","qtype":q,"archetype":A[n-1],"band":B[n-1],"gen":(gen_1,gen_2,gen_3,gen_4)[n-1],"ver":(ver_1,ver_2,ver_3,ver_4)[n-1],"stem_variants":S[n-1],"hints":H[n-1],"sol":SOL[n-1],**k}
TEMPLATES=[_t(1,"MC7",fmt=r"$@X@$",rats=RATS),_t(2,"FIB"),_t(3,"FIB"),_t(4,"MS",assumption_id="A-Hab01-01")]
```
</example>
<example>
```python
def ver_2(c,v):return abs(_pv(c)-v["x"])<1e-4
```
</example>
<instructions>
1. `read_file` author_XX.json. 2. `write_file` `<work_dir>/shards/<shard_id>_data.py`.
3. `run_command`: `python .agents/skills/content-to-course/compile_shard.py --work "<work_dir>" --shard <shard_id> --strict --min-archetypes 4 --fail-total`
4. Err: `<6` `edit_file`; `>=6` `shard_fixes/<CID>.py`. `BLOCKED:`. PASS->`DONE: <work_dir>/shards/<shard_id>.json`.
</instructions>
<constraints>
Verbosity: Low. Cero Asunciones: formulas/`assumption_id` solo de `author_XX.json`(si no hay,omitir).
</constraints>