cd sobel
./build.sh
cd ../sobel_extism
./build.sh
cd ../noop
./build.sh
cd ../malicious
./build.sh
cd ..
mv *.wasm ../image-processing-webservice/instance/operators/

