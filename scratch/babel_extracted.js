
    const { useState, useEffect } = React;

    const FadeIn = ({ children, delay = 0, duration = 1000, className = "" }) => {
      const [visible, setVisible] = useState(false);
      
      useEffect(() => {
        const timer = setTimeout(() => {
          setVisible(true);
        }, delay);
        return () => clearTimeout(timer);
      }, [delay]);

      return (
        <div 
          className={`transition-opacity ${className}`} 
          style={{ opacity: visible ? 1 : 0, transitionDuration: `${duration}ms` }}
        >
          {children}
        </div>
      );
    };

    const AnimatedHeading = ({ text, initialDelay = 200, charDelay = 30, className = "" }) => {
      const [startAnim, setStartAnim] = useState(false);
      
      useEffect(() => {
        const timer = setTimeout(() => {
          setStartAnim(true);
        }, initialDelay);
        return () => clearTimeout(timer);
      }, [initialDelay]);

      const lines = text.split('\n');
      
      return (
        <h1 className={className} style={{ letterSpacing: '-0.04em' }}>
          {lines.map((line, lineIndex) => (
            <div key={lineIndex} className="block">
              {line.split('').map((char, charIndex) => {
                const isSpace = char === ' ';
                const displayChar = isSpace ? '\u00A0' : char;
                const delay = (lineIndex * line.length * charDelay) + (charIndex * charDelay);
                
                return (
                  <span
                    key={charIndex}
                    className="inline-block transition-all"
                    style={{
                      opacity: startAnim ? 1 : 0,
                      transform: startAnim ? 'translateX(0)' : 'translateX(-18px)',
                      transitionDuration: '500ms',
                      transitionDelay: `${delay}ms`,
                      width: isSpace ? '0.3em' : 'auto'
                    }}
                  >
                    {displayChar}
                  </span>
                );
              })}
            </div>
          ))}
        </h1>
      );
    };

    const LoginApp = () => {
      const [showModal, setShowModal] = useState(false);

      return (
        <div className="relative w-full h-screen overflow-hidden bg-black text-white font-sans">
          <video autoPlay muted loop playsInline className="absolute inset-0 w-full h-full object-cover">
            <source src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260403_050628_c4e32401-fab4-4a27-b7a8-6e9291cd5959.mp4" type="video/mp4" />
          </video>
          
          <nav className="fixed top-0 left-0 right-0 z-50 px-6 md:px-12 lg:px-16 pt-6">
            <div className="liquid-glass rounded-xl px-4 py-2 flex items-center justify-between">
              <div className="text-2xl font-semibold tracking-tight">AGRIPAM</div>
              <div className="hidden md:flex gap-8">
                <a href="#" className="text-sm text-gray-300 hover:text-white transition-colors">Pemantauan</a>
                <a href="#" className="text-sm text-gray-300 hover:text-white transition-colors">Operasional</a>
                <a href="#" className="text-sm text-gray-300 hover:text-white transition-colors">Sistem</a>
                <a href="#" className="text-sm text-gray-300 hover:text-white transition-colors">Bantuan</a>
              </div>
              <button onClick={() => setShowModal(true)} className="bg-white text-black px-6 py-2 rounded-lg text-sm font-medium hover:bg-gray-100 transition-colors">
                Masuk ke Sistem
              </button>
            </div>
          </nav>

          <div className="relative z-10 w-full h-full px-6 md:px-12 lg:px-16 pb-12 lg:pb-16 flex flex-col justify-end">
            <div className="lg:grid lg:grid-cols-2 lg:items-end w-full">
              <div>
                <AnimatedHeading 
                  text={"Membangun masa depan\ndengan visi dan presisi."} 
                  className="text-4xl md:text-5xl lg:text-6xl xl:text-7xl font-normal mb-4"
                />
                
                <FadeIn delay={800} duration={1000}>
                  <p className="text-base md:text-lg text-gray-300 mb-5 max-w-xl">
                    Kami mendukung operasional perkebunan yang mendefinisikan standar masa depan.
                  </p>
                </FadeIn>
                
                <FadeIn delay={1200} duration={1000} className="flex flex-wrap gap-4">
                  <button onClick={() => setShowModal(true)} className="bg-white text-black px-8 py-3 rounded-lg font-medium hover:bg-gray-100 transition-colors">
                    Masuk ke Sistem
                  </button>
                  <button className="liquid-glass border border-white/20 text-white px-8 py-3 rounded-lg font-medium hover:bg-white hover:text-black transition-all">
                    Pelajari Lebih Lanjut
                  </button>
                </FadeIn>
              </div>

              <FadeIn delay={1400} duration={1000} className="hidden lg:flex items-end justify-end mt-8 lg:mt-0">
                <div className="liquid-glass border border-white/20 px-6 py-3 rounded-xl">
                  <span className="text-lg md:text-xl lg:text-2xl font-light">Pemantauan. Evaluasi. Agronomi.</span>
                </div>
              </FadeIn>
            </div>
          </div>

          {/* Login Modal Overlay */}
          <div className={`fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm transition-opacity duration-500 ${showModal ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'}`}>
            <div className={`liquid-glass rounded-2xl p-8 w-[90%] max-w-md transform transition-transform duration-500 border border-white/20 ${showModal ? 'scale-100' : 'scale-95'}`}>
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h2 className="text-2xl font-semibold text-white tracking-tight">Otentikasi Wilayah</h2>
                  <p className="text-gray-300 text-sm mt-1">Sistem Pemantauan Terpadu AGRIPAM</p>
                </div>
                <button onClick={() => setShowModal(false)} className="text-gray-400 hover:text-white transition-colors p-1">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
              </div>
              
              <form id="loginForm" noValidate onSubmit={(e) => { e.preventDefault(); window.prosesLogin(); }} className="flex flex-col gap-4">
                <div>
                  <label className="block text-gray-300 text-sm mb-2">Region / Wilayah</label>
                  <div className="relative">
                    <select id="loginRegion" required className="w-full bg-black/30 border border-white/20 text-white text-sm rounded-lg px-4 py-3 appearance-none focus:outline-none focus:border-white/50">
                      <option value="" disabled selected className="text-black">Pilih wilayah kerja...</option>
                      <option value="Aceh" className="text-black">Aceh</option>
                      <option value="Sumatera Utara 1" className="text-black">Sumatera Utara 1</option>
                      <option value="Sumatera Utara 2 Ex Torganda" className="text-black">Sumatera Utara 2 Ex Torganda</option>
                      <option value="Riau 1" className="text-black">Riau 1</option>
                      <option value="Riau 2" className="text-black">Riau 2</option>
                      <option value="Riau 3" className="text-black">Riau 3</option>
                      <option value="Riau 4" className="text-black">Riau 4</option>
                      <option value="Bangka Belitung" className="text-black">Bangka Belitung</option>
                      <option value="Jambi" className="text-black">Jambi</option>
                      <option value="Sumatera Barat" className="text-black">Sumatera Barat</option>
                      <option value="Sumatera Selatan" className="text-black">Sumatera Selatan</option>
                      <option value="Kalimantan Barat 1" className="text-black">Kalimantan Barat 1</option>
                      <option value="Kalimantan Barat 2" className="text-black">Kalimantan Barat 2</option>
                      <option value="Kalimantan Selatan 1" className="text-black">Kalimantan Selatan 1</option>
                      <option value="Kalimantan Selatan 2" className="text-black">Kalimantan Selatan 2</option>
                      <option value="Kalimantan Timur" className="text-black">Kalimantan Timur</option>
                      <option value="Kalimantan Utara" className="text-black">Kalimantan Utara</option>
                      <option value="Kalimantan Tengah 1" className="text-black">Kalimantan Tengah 1</option>
                      <option value="Kalimantan Tengah 2" className="text-black">Kalimantan Tengah 2</option>
                      <option value="Kalimantan Tengah 3" className="text-black">Kalimantan Tengah 3</option>
                      <option value="Sulawesi Tenggara" className="text-black">Sulawesi Tenggara</option>
                      <option value="Sulawesi Tengah" className="text-black">Sulawesi Tengah</option>
                      <option value="ADMIN" className="text-black">ADMIN</option>
                    </select>
                    <svg className="absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
                  </div>
                </div>

                <div>
                  <label className="block text-gray-300 text-sm mb-2">Password</label>
                  <input type="password" id="loginPassword" placeholder="Masukkan password" required className="w-full bg-black/30 border border-white/20 text-white placeholder-gray-500 text-sm rounded-lg px-4 py-3 focus:outline-none focus:border-white/50" />
                </div>

                <p className="text-red-400 text-xs hidden" id="loginError" role="alert"></p>

                <button type="submit" id="loginBtn" className="mt-2 w-full bg-white text-black font-semibold rounded-lg px-4 py-3 hover:bg-gray-100 transition-colors flex items-center justify-center gap-2">
                  <span className="btn-label">Masuk ke Sistem</span>
                </button>
              </form>
            </div>
          </div>
        </div>
      );
    };

    const root = ReactDOM.createRoot(document.getElementById('loginSectionRoot'));
    root.render(<LoginApp />);
  