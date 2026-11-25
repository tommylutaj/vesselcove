( function () {

	class USDZExporter {

		async parse( scene ) {

			let output = buildHeader();
			const materials = {};
			const textures = {};
			const textureHasAlpha = {};
			scene.traverse( object => {

				if ( object.isMesh ) {

					const geometry = object.geometry;
					const material = object.material;
					materials[ material.uuid ] = material;
					if ( material.map !== null ) {
						textures[ material.map.uuid ] = material.map;
						if ( material.transparent || material.alphaTest > 0 ) {
							textureHasAlpha[ material.map.uuid ] = true;
						}
					}
					if ( material.normalMap !== null ) textures[ material.normalMap.uuid ] = material.normalMap;
					if ( material.aoMap !== null ) textures[ material.aoMap.uuid ] = material.aoMap;
					if ( material.roughnessMap !== null ) textures[ material.roughnessMap.uuid ] = material.roughnessMap;
					if ( material.metalnessMap !== null ) textures[ material.metalnessMap.uuid ] = material.metalnessMap;
					if ( material.emissiveMap !== null ) textures[ material.emissiveMap.uuid ] = material.emissiveMap;
					output += buildXform( object, buildMesh( geometry, material ) );

				}

			} );
			output += buildMaterials( materials, textureHasAlpha );
			output += buildTextures( textures, textureHasAlpha );
			const files = {
				'model.usda': fflate.strToU8( output )
			};

			for ( const uuid in textures ) {

				const texture = textures[ uuid ];
				const usePng = !!textureHasAlpha[ uuid ];
				const ext = usePng ? 'png' : 'jpg';
				files[ 'textures/Texture_' + texture.id + '.' + ext ] = await imgToU8( texture.image, usePng );

			} // 64 byte alignment for Apple AR Quick Look USDZ
			// Local File Header = 30 + fnLen + (4 + padLen if extra added)


			let offset = 0;

			for ( const filename in files ) {

				const file = files[ filename ];
				const fnLen = fflate.strToU8( filename ).length;
				const baseOffset = offset + 30 + fnLen;
				let extraLen = 0;

				if ( ( baseOffset & 63 ) !== 0 ) {

					const padLength = ( 64 - ( ( baseOffset + 4 ) & 63 ) ) & 63;
					const padding = new Uint8Array( padLength );
					files[ filename ] = [ file, {
						extra: {
							12345: padding
						}
					} ];
					extraLen = 4 + padLength;

				}

				offset += 30 + fnLen + extraLen + file.length;

			}

			return fflate.zipSync( files, {
				level: 0
			} );

		}

	}

	async function imgToU8( image, usePng ) {

		if ( typeof HTMLImageElement !== 'undefined' && image instanceof HTMLImageElement || typeof HTMLCanvasElement !== 'undefined' && image instanceof HTMLCanvasElement || typeof OffscreenCanvas !== 'undefined' && image instanceof OffscreenCanvas || typeof ImageBitmap !== 'undefined' && image instanceof ImageBitmap ) {

			const scale = 1024 / Math.max( image.width, image.height );
			const canvas = document.createElement( 'canvas' );
			canvas.width = Math.max( 1, Math.round( image.width * Math.min( 1, scale ) ) );
			canvas.height = Math.max( 1, Math.round( image.height * Math.min( 1, scale ) ) );
			const context = canvas.getContext( '2d' );
			context.drawImage( image, 0, 0, canvas.width, canvas.height );
			const mime = usePng ? 'image/png' : 'image/jpeg';
			const blob = await new Promise( resolve => canvas.toBlob( resolve, mime, 0.96 ) );
			return new Uint8Array( await blob.arrayBuffer() );

		}

	} //


	const PRECISION = 7;

	function buildHeader() {

		return `#usda 1.0
(
    customLayerData = {
        string creator = "Three.js USDZExporter"
    }
    metersPerUnit = 1
    upAxis = "Y"
)

`;

	} // Xform


	function buildXform( object, define ) {

		const name = 'Object_' + object.id;
		const transform = buildMatrix( object.matrixWorld );
		return `def Xform "${name}"
{
    matrix4d xformOp:transform = ${transform}
    uniform token[] xformOpOrder = ["xformOp:transform"]

    ${define}
}

`;

	}

	function buildMatrix( matrix ) {

		const array = matrix.elements;
		return `( ${buildMatrixRow( array, 0 )}, ${buildMatrixRow( array, 4 )}, ${buildMatrixRow( array, 8 )}, ${buildMatrixRow( array, 12 )} )`;

	}

	function buildMatrixRow( array, offset ) {

		return `(${array[ offset + 0 ]}, ${array[ offset + 1 ]}, ${array[ offset + 2 ]}, ${array[ offset + 3 ]})`;

	} // Mesh


	function buildMesh( geometry, material ) {

		const name = 'Geometry_' + geometry.id;
		const attributes = geometry.attributes;
		const count = attributes.position.count;

		if ( 'uv2' in attributes ) {

			console.warn( 'THREE.USDZExporter: uv2 not supported yet.' );

		}

		const doubleSidedLine = material.side === THREE.DoubleSide ? '\n        uniform bool doubleSided = 1' : '';
		return `def Mesh "${name}"
    {
        int[] faceVertexCounts = [${buildMeshVertexCount( geometry )}]
        int[] faceVertexIndices = [${buildMeshVertexIndices( geometry )}]
        rel material:binding = </Materials/Material_${material.id}>
        normal3f[] normals = [${buildVector3Array( attributes.normal, count )}] (
            interpolation = "vertex"
        )
        point3f[] points = [${buildVector3Array( attributes.position, count )}]
        float2[] primvars:st = [${buildVector2Array( attributes.uv, count )}] (
            interpolation = "vertex"
        )${doubleSidedLine}
        uniform token subdivisionScheme = "none"
    }
`;

	}

	function buildMeshVertexCount( geometry ) {

		const count = geometry.index !== null ? geometry.index.array.length : geometry.attributes.position.count;
		return Array( count / 3 ).fill( 3 ).join( ', ' );

	}

	function buildMeshVertexIndices( geometry ) {

		if ( geometry.index !== null ) {

			return geometry.index.array.join( ', ' );

		}

		const array = [];
		const length = geometry.attributes.position.count;

		for ( let i = 0; i < length; i ++ ) {

			array.push( i );

		}

		return array.join( ', ' );

	}

	function buildVector3Array( attribute, count ) {

		if ( attribute === undefined ) {

			console.warn( 'USDZExporter: Normals missing.' );
			return Array( count ).fill( '(0, 0, 0)' ).join( ', ' );

		}

		const array = [];
		const data = attribute.array;

		for ( let i = 0; i < data.length; i += 3 ) {

			array.push( `(${data[ i + 0 ].toPrecision( PRECISION )}, ${data[ i + 1 ].toPrecision( PRECISION )}, ${data[ i + 2 ].toPrecision( PRECISION )})` );

		}

		return array.join( ', ' );

	}

	function buildVector2Array( attribute, count ) {

		if ( attribute === undefined ) {

			console.warn( 'USDZExporter: UVs missing.' );
			return Array( count ).fill( '(0, 0)' ).join( ', ' );

		}

		const array = [];
		const data = attribute.array;

		for ( let i = 0; i < data.length; i += 2 ) {

			array.push( `(${Number( data[ i + 0 ] ).toPrecision( PRECISION )}, ${Number( data[ i + 1 ] ).toPrecision( PRECISION )})` );

		}

		return array.join( ', ' );

	} // Materials


	function buildMaterials( materials, textureHasAlpha ) {

		const array = [];

		for ( const uuid in materials ) {

			const material = materials[ uuid ];
			array.push( buildMaterial( material, textureHasAlpha ) );

		}

		return `def "Materials"
{
${array.join( '' )}
}

`;

	}

	function buildMaterial( material, textureHasAlpha ) {

		// https://graphics.pixar.com/usd/docs/UsdPreviewSurface-Proposal.html
		const pad = '            ';
		const parameters = [];

		if ( material.map !== null ) {

			parameters.push( `${pad}color3f inputs:diffuseColor.connect = </Textures/Texture_${material.map.id}.outputs:rgb>` );

		} else {

			parameters.push( `${pad}color3f inputs:diffuseColor = ${buildColor( material.color )}` );

		}

		if ( material.emissiveMap !== null ) {

			parameters.push( `${pad}color3f inputs:emissiveColor.connect = </Textures/Texture_${material.emissiveMap.id}.outputs:rgb>` );

		} else if ( material.emissive.getHex() > 0 ) {

			parameters.push( `${pad}color3f inputs:emissiveColor = ${buildColor( material.emissive )}` );

		}

		if ( material.normalMap !== null ) {

			parameters.push( `${pad}normal3f inputs:normal.connect = </Textures/Texture_${material.normalMap.id}.outputs:rgb>` );

		}

		if ( material.aoMap !== null ) {

			parameters.push( `${pad}float inputs:occlusion.connect = </Textures/Texture_${material.aoMap.id}.outputs:r>` );

		}

		if ( material.roughnessMap !== null ) {

			parameters.push( `${pad}float inputs:roughness.connect = </Textures/Texture_${material.roughnessMap.id}.outputs:g>` );

		} else {

			parameters.push( `${pad}float inputs:roughness = ${material.roughness}` );

		}

		if ( material.metalnessMap !== null ) {

			parameters.push( `${pad}float inputs:metallic.connect = </Textures/Texture_${material.metalnessMap.id}.outputs:b>` );

		} else {

			parameters.push( `${pad}float inputs:metallic = ${material.metalness}` );

		}

		if ( material.map !== null && textureHasAlpha && textureHasAlpha[ material.map.uuid ] ) {

			parameters.push( `${pad}float inputs:opacity.connect = </Textures/Texture_${material.map.id}.outputs:a>` );
			if ( material.alphaTest > 0 ) {
				parameters.push( `${pad}float inputs:opacityThreshold = ${material.alphaTest}` );
			}

		} else if ( material.transparent === true || material.opacity < 1.0 ) {

			parameters.push( `${pad}float inputs:opacity = ${material.opacity}` );

		}

		if ( typeof material.clearcoat === 'number' && material.clearcoat > 0 ) {

			parameters.push( `${pad}float inputs:clearcoat = ${material.clearcoat}` );
			if ( typeof material.clearcoatRoughness === 'number' ) {
				parameters.push( `${pad}float inputs:clearcoatRoughness = ${material.clearcoatRoughness}` );
			}

		}

		return `
    def Material "Material_${material.id}"
    {
        token outputs:surface.connect = </Materials/Material_${material.id}/PreviewSurface.outputs:surface>

        def Shader "PreviewSurface"
        {
            uniform token info:id = "UsdPreviewSurface"
${parameters.join( '\n' )}
            int inputs:useSpecularWorkflow = 0
            token outputs:surface
        }
    }
`;

	}

	function buildTextures( textures, textureHasAlpha ) {

		const array = [];

		for ( const uuid in textures ) {

			const texture = textures[ uuid ];
			array.push( buildTexture( texture, !!( textureHasAlpha && textureHasAlpha[ uuid ] ) ) );

		}

		return `def "Textures"
{
${array.join( '' )}
}

`;

	}

	function buildTexture( texture, usePng ) {

		const ext = usePng ? 'png' : 'jpg';
		return `
    def Shader "Texture_${texture.id}"
    {
        uniform token info:id = "UsdUVTexture"
        asset inputs:file = @textures/Texture_${texture.id}.${ext}@
        token inputs:wrapS = "repeat"
        token inputs:wrapT = "repeat"
        float outputs:r
        float outputs:g
        float outputs:b
        float outputs:a
        float3 outputs:rgb
    }
`;

	}

	function buildColor( color ) {

		return `(${color.r}, ${color.g}, ${color.b})`;

	}

	THREE.USDZExporter = USDZExporter;

} )();
