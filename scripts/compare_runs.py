"""Compara tabelas de execução isolada com artefatos preservados."""
from collections import Counter
from pathlib import Path
import argparse,json
import csv
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[1]


def _read_csv_counts(path):
    with path.open(encoding='utf-8-sig', newline='') as file:
        reader = csv.reader(file, strict=True)
        columns = next(reader, None)
        if not columns:
            raise ValueError(f'Cabeçalho CSV ausente em {path}.')

        counts = Counter()
        for row in reader:
            if len(row) != len(columns):
                raise ValueError(f'Quantidade de campos inválida em {path}, linha {reader.line_num}.')
            counts[tuple(row)] += 1
    return columns, counts


def _compare_outlier_coincidence(historical, reproduced):
    historical_columns, historical_rows = _read_csv_counts(historical)
    reproduced_columns, reproduced_rows = _read_csv_counts(reproduced)
    if historical_columns != reproduced_columns:
        raise ValueError(f'Colunas diferentes: {historical_columns!r} e {reproduced_columns!r}.')
    if historical_rows != reproduced_rows:
        missing = (historical_rows - reproduced_rows).total()
        added = (reproduced_rows - historical_rows).total()
        raise ValueError(f'Valores ou multiplicidades diferentes: {missing} ocorrência(s) ausente(s) e {added} adicional(is).')
    return historical_rows.total()


def compare(run):
 rows=[]
 for f in sorted((ROOT/'outputs/tables').glob('*.csv')):
  other=run/'outputs/tables'/f.name
  if not other.exists():rows.append({'file':f.name,'status':'missing'});continue
  try:
   if f.name == 'outlier_coincidence.csv':
    row_count = _compare_outlier_coincidence(f, other)
   else:
    a=pd.read_csv(f);b=pd.read_csv(other)
    pd.testing.assert_frame_equal(a,b,check_dtype=False,check_exact=False,rtol=1e-7,atol=1e-7)
    row_count = len(a)
   rows.append({'file':f.name,'status':'equivalent','rows':row_count,'byte_equal':f.read_bytes()==other.read_bytes()})
  except Exception as e:rows.append({'file':f.name,'status':'different','detail':str(e)[:1800]})
 return rows
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('run',type=Path);args=ap.parse_args();rows=compare(args.run.resolve())
 out=ROOT/'docs/proveniencia/comparacao_reexecucao.json';out.write_text(json.dumps({'rtol':1e-7,'atol':1e-7,'tables':rows},ensure_ascii=False,indent=2))
 print(pd.Series([r['status'] for r in rows]).value_counts().to_string())
 for r in rows:
  if r['status']!='equivalent':print(r)
