"""Executa o notebook canônico; full sempre usa cópia isolada dos históricos."""
import argparse, os, shutil, tempfile, json, traceback, io, contextlib
from pathlib import Path
import nbformat
from nbclient import NotebookClient

ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=['temporal','full'],default='temporal');ap.add_argument('--isolated',action='store_true');ap.add_argument('--engine',choices=['jupyter','inprocess'],default='jupyter');args=ap.parse_args()
    isolated=args.isolated or args.mode=='full'
    if isolated:
        target=ROOT/'validation_runs'/next(tempfile._get_candidate_names());target.mkdir(parents=True)
        for name in ['data','outputs','docs','notebooks']:
            shutil.copytree(ROOT/name,target/name,ignore=shutil.ignore_patterns('.mplcache'))
        for name in ['.tcc-mmm-root','requirements.txt','requirements-temporal.txt']:shutil.copyfile(ROOT/name,target/name)
    else:target=ROOT
    os.environ['TCC_MMM_ROOT']=str(target)
    nb=nbformat.read(ROOT/'notebooks/01_EDA_COMPLETA.ipynb',as_version=4)
    start=122 if args.mode=='temporal' else 0
    original=nb.cells[:start];nb.cells=nb.cells[start:]
    # Execute em kernel novo. Outputs originais nunca são substituídos no notebook publicado.
    client=NotebookClient(nb,timeout=1800,kernel_name='python3',resources={'metadata':{'path':str(target)}})
    try:
        if args.engine=='jupyter':
            client.execute()
        else:
            # Alternativa explícita para hosts sem sockets ZMQ. Não equivale à interface Colab.
            from IPython.core.interactiveshell import InteractiveShell
            from IPython.utils.capture import capture_output
            shell=InteractiveShell.instance()
            shell.user_ns['__name__']='__main__'
            os.chdir(target)
            count=0
            for idx,cell in enumerate(nb.cells,start):
                if cell.cell_type!='code':continue
                count+=1
                print(f'Executando célula {idx}',flush=True)
                with capture_output() as captured:
                    result=shell.run_cell(cell.source,store_history=True)
                cell.outputs=[];cell.execution_count=count
                if captured.stdout:cell.outputs.append(nbformat.v4.new_output('stream',name='stdout',text=captured.stdout))
                if captured.stderr:cell.outputs.append(nbformat.v4.new_output('stream',name='stderr',text=captured.stderr))
                for output in captured.outputs:
                    cell.outputs.append(nbformat.v4.new_output('display_data',data=output.data,metadata=output.metadata))
                if result.error_before_exec or result.error_in_exec:
                    print(captured.stdout, captured.stderr,flush=True)
                    raise result.error_before_exec or result.error_in_exec

    finally:
        if args.mode=='temporal' and not isolated:
            nb.cells=original+nb.cells;nbformat.write(nb,ROOT/'notebooks/01_EDA_COMPLETA.ipynb')
        else:nbformat.write(nb,target/'executed.ipynb')
        print('Diretório da execução:',target,flush=True)
if __name__=='__main__':main()
