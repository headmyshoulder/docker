#! /usr/bin/python

import sys
import subprocess
import argparse
import os

description = """Create docker images."""

directory = os.path.abspath( os.path.dirname( __file__ ) )

images = [
    [ "karsten/ssh-base" , "docker-base" ]
  , [ "karsten/java-base" , "docker-java" ]
  ]


def run_cmd( cmd ):
    # print cmd
    return subprocess.call( cmd , shell=True )


def run_cmd_output( cmd ):
    process = subprocess.Popen( cmd  , shell=True , stdout=subprocess.PIPE )
    out , err = process.communicate()
    return process.returncode , out

def error( msg ):
    print "Error: " + msg
    exit( -1 )

def warning( msg ):
    print "Warning: " + msg



def parseCmd( argv ):
    parser = argparse.ArgumentParser( description = description , formatter_class = argparse.ArgumentDefaultsHelpFormatter )
    subparsers = parser.add_subparsers( title = "commands" , dest = "command" )
    
    createParser = subparsers.add_parser( "create" , help = "Run the cluster." )
    createParser.add_argument( "image" , help="Image to create. 'all' create all possible images." , nargs='?' , default="all" , type=str )
    
    rmParser = subparsers.add_parser( "rmi" , help = "Start the cluster." )
    rmParser.add_argument( "image" , help="Image to remove. 'all' removes all possible images." , nargs='?' , default="all" , type=str )

    rmParser = subparsers.add_parser( "rm" , help = "Start the cluster." )
    rmParser.add_argument( "image" , help="Remove all container from a specific image. 'all' removes all possible images." , nargs='?' , default="all" , type=str )

    listParser = subparsers.add_parser( "list" , help="Show all images." )

    args = parser.parse_args( argv[1:] )
    return args


def show_list( args ):
    for image in images:
        print "%-20s  -  Dockerfile is in %s" % ( image[0] , os.path.join( directory , image[1] ) )

def create_image( args , image ):
    os.chdir( directory )
    print "Creatimg image " + image[0]
    os.chdir( os.path.join( directory , image[1] ) )
    ret = run_cmd( "docker build -t " + image[0] + " . " )
    if ret != 0:
        error( "Could not build " + image[0] + " at " + os.path.join( directory ) )

def create( args ):
    if args.image == "all":
        for image in images:
            create_image( args , image )
    else:
        create_image( args , args.image )

def rmi_image( args , image ):
    os.chdir( directory )
    print "Removing image " + image[0]
    ret = run_cmd( "docker rmi " + image[0] )
    if ret != 0:
        error( "Could not remove " + image[0] )

def rmi( args ):
    if args.image == "all":
        for image in images:
            rmi_image( args , image )
    else:
        rmi_image( args , args.image )

def rm_image( args , image ):
    os.chdir( directory )
    print "Removing image " + image[0]
    ret , out = run_cmd_output( "docker ps -a | grep " + image[0] )
    if ret != 0:
        warning( "Could not remove container from image " + image[0] )
    for lines in out.split( "\n" ):
        splitted = lines.split()
        if len( splitted ) == 0:
            continue
        id = splitted[0]
        print id
        ret = run_cmd( "docker stop " + str( id ) )
        if ret != 0:
            warning( "Could not remove containers from " + image[0] )
            continue
        ret = run_cmd( "docker rm " + str( id ) )
        if ret != 0:
            warning( "Could not remove containers from " + image[0] )
            continue


def rm( args ):
    if args.image == "all":
        for image in images:
            rm_image( args , image )
    else:
        rm_image( args , args.image )


def main( argv ):
    
    args = parseCmd( argv )
        
    if args.command == "create":
        create( args )
    if args.command == "rmi":
        rmi( args )
    if args.command == "rm":
        rm( args )
    if args.command == "list":
        show_list( args )


if __name__ == "__main__" :
    main( sys.argv )
