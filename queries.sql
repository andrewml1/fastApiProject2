-- ##Conteo normal
select distinct
    Via,
    count(*)
from evaluaciones
group by 1;

-- Conteo por evaluaciones
select distinct
Via,
count(ID) conteo
from evaluaciones
group by 1;


-- ##Numero de evaluaciones
select
case
    when e.Evaluacion ='' then 'No tratamiento'
    else e.Evaluacion
    end as Evaluacion,
e.Via,
count (p.ID) as conteo
from paciente p
left join evaluaciones e on p.ID = e.ID
group by 1,2;
-- having Via not null;


------------------------- QUERY MONTE CARLO ------------------------- QUERY MONTE CARLO------------------------- QUERY MONTE CARLO
select
date() as Fecha,
-- :numIteracionMC as NumMC,
'11' as NumMC,
p.*,
e.Tipo,
e.Via,
e.Evaluacion
from paciente p
left join evaluaciones e on p.ID = e.ID
where p.ID>=26623;
-----------------------------------------------------------------------------------------------------------------------------

with tb_maxID as (
        SELECT MAX(ID) ID,
        p.*
        FROM paciente p
)
select
date() as Fecha,
'6' as NumMC,
p.*,
e.*,
case
    when LEAD(Evaluacion) OVER (ORDER BY Via) =null then ''
    else LEAD(Evaluacion) OVER (ORDER BY Via)
    end
    AS prev_Eval
from tb_maxID p
left join evaluaciones e on p.ID = e.ID
where p.ID>1012;



--Query validaciones / alertas
with tb_flacos as (
select
date() as Fecha,
p.*,
e.Tipo,
e.Via,
e.Evaluacion,
'Flacos insulina' as Alerta
from paciente p
left join evaluaciones e on p.ID = e.ID
where p.imc<22 and e.Evaluacion like '%insulina%'and p.ID>10000),
tb_fallaBeta as (
    select
    date() as Fecha,
    p.*,
    e.Tipo,
    e.Via,
    e.Evaluacion,
    'Falla celula beta' as Alerta
    from paciente p
    left join evaluaciones e on p.ID = e.ID
    where e.Evaluacion like '%risk hipogl%'and e.Evaluacion not like '%no insul%' and p.ID>10000
    ),
tb_subgrupo as (
--glp en el subgrupo mas intolerancia glp mas haba1c>8
    select
    date() as Fecha,
    p.*,
    e.Tipo,
    e.Via,
    e.Evaluacion,
    'Falla subgrupo' as Alerta
    from paciente p
    left join evaluaciones e on p.ID = e.ID
    where p.subGrupoMedicamento like '%aGLP%'and p.tolera_aGLP1 = 0 and p.hba1c>9
),
    tb_edadSospecha as (
    select
    date() as Fecha,
    p.*,
    e.Tipo,
    e.Via,
    e.Evaluacion,
    'Falla Edad' as Alerta
    from paciente p
    left join evaluaciones e on p.ID = e.ID
    where p.edad<35 and p.imc<30
),
    tb_insulinaBolo as (
    select
    date() as Fecha,
    p.*,
    e.Tipo,
    e.Via,
    e.Evaluacion,
    'Falla insulinaBolo' as Alerta
    from paciente p
    left join evaluaciones e on p.ID = e.ID
    where p.subGrupoMedicamento like '%Basa%Prand%'
)
, tbAlertas as (
    select *
    from tb_flacos
union all
    select *
    from tb_fallaBeta
union all
    select *
    from tb_subgrupo
union all
    select *
    from tb_edadSospecha
union all
    select *
    from tb_insulinaBolo
    )
select
    Alerta,
    count(distinct ID)
from tbAlertas where ID>22048
group by 1;


select
    count(distinct ID) --Total pacientes
from evaluaciones where ID>22048;



--ADOS con Insulina: 3 ados o mas e insulina
select
date() as Fecha,
p.*,
e.Tipo,
e.Via,
e.Evaluacion,
'ADOS con Insulina' as Alerta
from paciente p
left join evaluaciones e on p.ID = e.ID
where e.Evaluacion like '%risk hipogl%'and e.Evaluacion not like '%no insul%' and p.ID>10000







