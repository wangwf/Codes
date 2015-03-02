sudo docker run numenta/nupic /usr/local/src/nupic/scripts/run_nupic_tests -u --coverage
sudo docker run numenta/nupic /usr/local/src/nupic/bin/py_region_test

docker images

sudo docker run -i -t numenta/nupic /bin/bash -c "python /usr/local/src/nupic/examples/opf/clients/hotgym/simple/hotgym.py"

sudo docker run -i -t numenta/nupic /bin/bash -c "python /usr/local/src/nupic/scripts/run_opf_experiment.py /usr/local/src/nupic/examples/opf/experiments/multistep/hotgym/"

sudo docker run -i -t numenta/nupic /bin/bash
