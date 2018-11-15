void start(){
	
	print("Reading ...");
	secret(0x1000);
	
	while (true){
		sp -= 32;
		write("enter a code");
		read(sp, 0x40);
		
		if is_same(sp, 0x1000, 32){
			exit();
		}
	}
	
}