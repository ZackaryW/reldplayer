import pprint
import click
from pyldplayer.coms.batchConsole import LDBatchConsole
from pyldplayer.utils.query import QueryObj
from pyldplayer.model.list2meta import List2Meta
from click.core import Context


try:
    console = LDBatchConsole()
except:  # noqa
    console = None

def get_3_affected(queryobj : QueryObj):
    res = console.query(queryobj)
    for item in res:
        yield item["name"] + "(" + str(item["id"]) + ")"

def get_affected_string(queryobj : QueryObj):
    string : str = ""
    for item in get_3_affected(queryobj):
        if len(string) > 25:
            string += ", ..."
            break
        string += item + ", "
    return string

class CustomGroup(click.Group):
    def format_commands(self, ctx: Context, formatter: click.HelpFormatter) -> None:
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            if cmd is None or cmd.hidden:
                continue
            commands.append((subcommand, cmd))

        # Format commands in rows of 3
        if commands:
            rows = []
            current_row = []
            
            # Find the maximum length for padding
            max_len = max(len(cmd) for cmd, _ in commands)
            
            for i, (subcommand, cmd) in enumerate(commands):
                # Pad each command with spaces to ensure consistent width
                padded_command = subcommand.ljust(max_len)
                current_row.append(padded_command)
                if len(current_row) == 3:  # Split every 3 commands
                    rows.append(current_row)
                    current_row = []
            
            if current_row:  # Add any remaining commands
                while len(current_row) < 3:  # Pad with empty strings
                    current_row.append(" " * max_len)
                rows.append(current_row)

            with formatter.section('Commands'):
                for row in rows:
                    formatter.write('  ' + '\t\t'.join(row))
                    formatter.write('\n')

@click.group(cls=CustomGroup, invoke_without_command=True)
@click.option("--query", "-q", help="query spec")
@click.option("--id", "-i", help="specifc id", type=int)
@click.option("--name", "-n", help="specifc name")
@click.option("--path", "-p", help="console path")
@click.option("--interval", "-I", help="interval")
@click.option("--do-not-wait", "-D", is_flag=True, help="do not use interval")
@click.pass_context
def cli(
    ctx: click.Context,
    query: str,
    id: int,
    name: str,
    path: str,
    interval: int,
    do_not_wait: bool,
):
    if not ctx.invoked_subcommand:
        click.echo(ctx.get_help())

    global console
    if not console:
        if path:
            console = LDBatchConsole(path)
        else:
            raise click.UsageError("cannot resolve console")

    if not do_not_wait:
        interval = interval or 5
        console.add_interval(interval=interval)

    if query:
        query2 = query
    else:
        query2 = "True"

    if id:
        query2 += f" and id == {id}"

    if name:
        query2 += f" and name == {name}"
    
    try:
        ctx.obj = QueryObj.parse(query2)
    except Exception as e:
        raise click.UsageError(f"invalid query: {e}")



    click.echo(f"scope: {get_affected_string(ctx.obj)}")

@cli.command("list2")
def list2():
    click.echo("command: list2")
    click.echo("name\t\tid\ttwh\tbwh\tpid")
    for meta in console.list2():
        if meta["id"] == 0:
            continue
        meta : List2Meta    
        string = ""
        string += meta["name"] + "\t\t"
        string += str(meta["id"]) + "\t"
        string += str(meta["top_window_handle"]) + "\t"
        string += str(meta["bind_window_handle"]) + "\t"
        string += str(meta["pid"])
        click.echo(string)
#

@cli.command()
def rock():
    click.echo("command: rock")
    console.rock()

@cli.command()
def quitall():
    click.echo("command: quitall")
    console.quitall()

@cli.command()
def zoomOut():
    click.echo("command: zoomOut")
    console.zoomOut()

@cli.command()
def zoomIn():
    click.echo("command: zoomIn")
    console.zoomIn()

@cli.command()
def sortWnd():
    click.echo("command: sortWnd")
    console.sortWnd()

# 
@cli.command()
@click.pass_context
def quit(ctx: click.Context):
    click.echo("command: quit")
    console.quit(ctx.obj)

@cli.command()
@click.pass_context
def launch(ctx: click.Context):
    click.echo("command: launch")
    console.launch(ctx.obj)

@cli.command()
@click.pass_context
def reboot(ctx: click.Context):
    click.echo("command: reboot")
    console.reboot(ctx.obj)

#SECTION - 
@cli.command()
@click.option("--from", "-f", "from_", help="copy from this instance")
@click.pass_context
def copy(ctx: click.Context, from_: str):
    console.copy(ctx.obj, _from=from_)

@cli.command()
@click.option("--title", "-t", help="new title")
@click.pass_context
def rename(ctx: click.Context, title: str):
    console.rename(ctx.obj, title=title)

@cli.command()
@click.option("--package", "-p", required=True, help="package name")
@click.option("--file", "-f", required=True, help="apk file path")
@click.pass_context
def installapp(ctx: click.Context, package: str, file: str):
    console.installapp(ctx.obj, packagename=package, filename=file)

@cli.command()
@click.option("--package", "-p", required=True, help="package name")
@click.pass_context
def uninstallapp(ctx: click.Context, package: str):
    console.uninstallapp(ctx.obj, packagename=package)

@cli.command()
@click.option("--package", "-p", required=True, help="package name")
@click.pass_context
def runapp(ctx: click.Context, package: str):
    console.runapp(ctx.obj, packagename=package)

@cli.command()
@click.option("--package", "-p", required=True, help="package name")
@click.pass_context
def killapp(ctx: click.Context, package: str):
    console.killapp(ctx.obj, packagename=package)

@cli.command()
@click.option("--lli", "-l", required=True, help="LLI parameter")
@click.pass_context
def locate(ctx: click.Context, lli: str):
    console.locate(ctx.obj, LLI=lli)

@cli.command()
@click.option("--command", "-c", required=True, help="ADB command to execute")
@click.pass_context
def adb(ctx: click.Context, command: str):
    console.adb(ctx.obj, command=command)

@cli.command()
@click.option("--key", "-k", required=True, help="property key")
@click.option("--value", "-v", required=True, help="property value")
@click.pass_context
def setprop(ctx: click.Context, key: str, value: str):
    console.setprop(ctx.obj, key=key, value=value)

@cli.command()
@click.option("--rate", "-r", required=True, type=int, help="CPU rate")
@click.pass_context
def downcpu(ctx: click.Context, rate: int):
    console.downcpu(ctx.obj, rate=rate)

@cli.command()
@click.option("--file", "-f", required=True, help="backup file path")
@click.pass_context
def backup(ctx: click.Context, file: str):
    console.backup(ctx.obj, file=file)

@cli.command()
@click.option("--file", "-f", required=True, help="restore file path")
@click.pass_context
def restore(ctx: click.Context, file: str):
    console.restore(ctx.obj, file=file)

@cli.command()
@click.option("--key", "-k", required=True, help="action key")
@click.option("--value", "-v", required=True, help="action value")
@click.pass_context
def action(ctx: click.Context, key: str, value: str):
    console.action(ctx.obj, key=key, value=value)

@cli.command()
@click.option("--file", "-f", required=True, help="scan file path")
@click.pass_context
def scan(ctx: click.Context, file: str):
    console.scan(ctx.obj, file=file)

@cli.command()
@click.option("--remote", "-r", required=True, help="remote path")
@click.option("--local", "-l", required=True, help="local path")
@click.pass_context
def pull(ctx: click.Context, remote: str, local: str):
    console.pull(ctx.obj, remote=remote, local=local)

@cli.command()
@click.option("--remote", "-r", required=True, help="remote path")
@click.option("--local", "-l", required=True, help="local path")
@click.pass_context
def push(ctx: click.Context, remote: str, local: str):
    console.push(ctx.obj, remote=remote, local=local)

@cli.command()
@click.option("--package", "-p", required=True, help="package name")
@click.option("--file", "-f", required=True, help="backup file path")
@click.pass_context
def backupapp(ctx: click.Context, package: str, file: str):
    console.backupapp(ctx.obj, packagename=package, file=file)

@cli.command()
@click.option("--package", "-p", required=True, help="package name")
@click.option("--file", "-f", required=True, help="restore file path")
@click.pass_context
def restoreapp(ctx: click.Context, package: str, file: str):
    console.restoreapp(ctx.obj, packagename=package, file=file)

@cli.command()
@click.option("--package", "-p", required=True, help="package name")
@click.pass_context
def launchex(ctx: click.Context, package: str):
    console.launchex(ctx.obj, packagename=package)

@cli.command()
@click.option("--content", "-c", required=True, help="record content")
@click.pass_context
def operaterecord(ctx: click.Context, content: str):
    console.operaterecord(ctx.obj, content=content)

def run():
    cli()

if __name__ == "__main__":
    run()
